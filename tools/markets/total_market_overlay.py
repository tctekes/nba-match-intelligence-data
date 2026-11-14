"""Prospective NBA full-game O/U overlay; separate from frozen Model C.

This tool does not fetch, guess, or validate market quotations against external
websites. Input quote provenance MUST be collected and checked independently.
No use of outcome scores in build_overlay(); no re-fitting or probability tuning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

RULE_VERSION = "nba-ou-reviewed-direction-v0.2"
VALID_STAGE = {"NONE", "GROUP_PLAY", "QUARTERFINAL", "SEMIFINAL", "CHAMPIONSHIP"}
MARKET_KIND = "FULL_GAME_INCLUDING_OT"


def fail(message: str):
    raise ValueError(message)


def timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        fail("Missing UTC timestamp")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail("Invalid ISO timestamp")
    if dt.tzinfo is None or dt.utcoffset().total_seconds() != 0:
        fail("Timestamp must be explicitly UTC (Z or +00:00)")
    return dt.astimezone(timezone.utc)


def url(value: str, *, nba_official=False) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("Missing source URL")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        fail("Source URL must be https")
    if nba_official and parsed.hostname not in {"nba.com", "www.nba.com"}:
        fail("Cup status must be linked to official NBA schedule")
    return value


def fixture(obj: dict) -> str:
    away, home = obj.get("away"), obj.get("home")
    if not isinstance(away, str) or not isinstance(home, str) or len(away) != 3 or len(home) != 3 or away == home:
        fail("Invalid away/home team fixture")
    return f"{away}@{home}"


def unique_fixture_map(items: list, description: str) -> dict:
    if not isinstance(items, list):
        fail(f"{description} must be a list")
    result = {}
    for item in items:
        if not isinstance(item, dict):
            fail(f"{description} contains non-object")
        key = fixture(item)
        if key in result:
            fail(f"Duplicate {description}: {key}")
        result[key] = item
    return result


def numeric(value, description: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        fail(f"Invalid {description}")
    result = float(value)
    if not (-1e9 < result < 1e9):
        fail(f"Invalid/non-finite {description}")
    return result


def build_overlay(forecast: dict, market: dict, forecast_raw: bytes) -> dict:
    if forecast.get("status") != "LOCKED_PREGAME_SHADOW_NOT_PRODUCTION":
        fail("Input must be original locked pretip shadow forecast")
    if forecast.get("nba_local_date") != market.get("nba_local_date"):
        fail("NBA-local slate date mismatch")
    for key in ("model_file_sha256", "parameter_file_sha256", "current_snapshot_sha256"):
        val = forecast.get(key)
        if not isinstance(val, str) or len(val) != 64 or any(c not in "0123456789abcdef" for c in val):
            fail(f"Unverifiable model/snapshot checksum: {key}")
    forecasts = unique_fixture_map(forecast.get("games"), "model forecasts")
    cups = unique_fixture_map(market.get("cup_context"), "Cup context")
    quotes = unique_fixture_map(market.get("quotes"), "O/U market quotations")
    if not forecasts or set(cups) != set(forecasts) or not set(quotes).issubset(forecasts):
        fail("Cup context must cover all games, market quotes must match fixtures")
    forecast_time = timestamp(forecast.get("generated_at_utc"))
    rows = []
    for game_id, game in forecasts.items():
        tip = timestamp(game.get("tipoff_utc"))
        if forecast_time >= tip:
            fail(f"Forecast created after start: {game_id}")
        context = cups[game_id]
        is_cup = context.get("is_nba_cup")
        stage = context.get("cup_stage")
        if type(is_cup) is not bool or stage not in VALID_STAGE:
            fail(f"Missing or invalid Cup flag: {game_id}")
        if is_cup != (stage != "NONE"):
            fail(f"Contradictory Cup flag: {game_id}")
        group = context.get("cup_group")
        if stage == "GROUP_PLAY" and (not isinstance(group, str) or not group.strip()):
            fail(f"Missing Cup group: {game_id}")
        if stage == "NONE" and group is not None:
            fail(f"Unexpected Cup group: {game_id}")
        if timestamp(context.get("checked_at_utc")) >= tip:
            fail(f"Cup status checked after start: {game_id}")
        url(context.get("source_url"), nba_official=True)
        model_total = numeric(game.get("expected_full_game_total"), "model total")
        prediction_row = {
            "away": game["away"], "home": game["home"], "tipoff_utc": game["tipoff_utc"],
            "is_nba_cup": is_cup, "cup_stage": stage, "cup_group": group,
            "cup_source_url": context["source_url"],
            "model_predicted_winner": game.get("predicted_winner"),
            "model_winner_probability": numeric(game.get("win_probability"), "winner probability"),
            "model_expected_home_margin": numeric(game.get("expected_home_margin"), "home margin"),
            "model_expected_full_game_total": model_total,
            "market_status": "MARKET_NOT_VERIFIED", "market_kind": None,
            "bookmaker": None, "market_source_url": None, "market_captured_at_utc": None,
            "market_line": None, "over_decimal": None, "under_decimal": None,
            "delta": None, "raw_direction": None, "selected_direction": None,
            "analyst_confidence": None, "analyst_rationale": None, "analyst_reviewed_at_utc": None,
        }
        if game_id in quotes:
            q = quotes[game_id]
            if q.get("market_kind") != MARKET_KIND or q.get("is_main_line") is not True:
                fail(f"Incorrect O/U market, main line or OT settlement: {game_id}")
            if not isinstance(q.get("bookmaker"), str) or not q["bookmaker"].strip():
                fail(f"Unnamed bookmaker: {game_id}")
            url(q.get("source_url"))
            qt = timestamp(q.get("captured_at_utc"))
            if qt >= tip:
                fail(f"Quote captured after tipoff: {game_id}")
            line = numeric(q.get("line"), "market line")
            over = numeric(q.get("over_decimal"), "Over decimal odds")
            under = numeric(q.get("under_decimal"), "Under decimal odds")
            if line <= 0 or not (1.0 < over < 1000.0) or not (1.0 < under < 1000.0):
                fail(f"Invalid main-line and/or European decimal price: {game_id}")
            gap = round(model_total - line, 8)
            direction = "OVER" if gap > 0 else "UNDER" if gap < 0 else "NEUTRAL"
            review = q.get("analyst_review")
            if not isinstance(review, dict):
                fail(f"Analyst O/U direction and confidence review required: {game_id}")
            selected = review.get("direction")
            confidence = review.get("confidence")
            rationale = review.get("rationale")
            if selected not in {"OVER", "UNDER"} or confidence not in {"LOW", "MEDIUM", "HIGH"}:
                fail(f"Missing reviewed OVER/UNDER or LOW/MEDIUM/HIGH confidence: {game_id}")
            if not isinstance(rationale, str) or len(rationale.strip()) < 30:
                fail(f"Analyst must provide >=30-character evidence and counterargument: {game_id}")
            reviewed = timestamp(review.get("reviewed_at_utc"))
            if reviewed < qt or reviewed >= tip:
                fail(f"Analyst review must follow captured quote and precede tipoff: {game_id}")
            prediction_row.update(
                market_status="PRETIP_MAIN_LINE_QUOTED", market_kind=MARKET_KIND,
                bookmaker=q["bookmaker"], market_source_url=q["source_url"],
                market_captured_at_utc=q["captured_at_utc"], market_line=line,
                over_decimal=over, under_decimal=under, delta=gap,
                raw_direction=direction, selected_direction=selected,
                analyst_confidence=confidence, analyst_rationale=rationale.strip(),
                analyst_reviewed_at_utc=review["reviewed_at_utc"],
            )
        rows.append(prediction_row)
    return {
        "schema_version": "nba-ou-shadow-overlay-v2", "status": "LOCKED_SHADOW_NOT_PRODUCTION",
        "selection_rule_version": RULE_VERSION, "confidence_is_calibrated": False,
        "nba_local_date": forecast["nba_local_date"],
        "original_forecast_sha256": hashlib.sha256(forecast_raw).hexdigest(),
        "forecast_generated_at_utc": forecast["generated_at_utc"],
        "model": forecast.get("model"),
        "model_file_sha256": forecast["model_file_sha256"],
        "parameter_file_sha256": forecast["parameter_file_sha256"],
        "current_snapshot_sha256": forecast["current_snapshot_sha256"],
        "original_model_outputs_unchanged": True,
        "games": rows,
    }


def grade_overlay(overlay: dict, finals: dict) -> dict:
    if overlay.get("status") != "LOCKED_SHADOW_NOT_PRODUCTION" or overlay.get("schema_version") != "nba-ou-shadow-overlay-v2":
        fail("Expected original locked O/U overlay")
    if overlay.get("nba_local_date") != finals.get("nba_local_date"):
        fail("Retrospective NBA date mismatch")
    games = unique_fixture_map(overlay.get("games"), "O/U overlay")
    results = unique_fixture_map(finals.get("results"), "game finals")
    if not games or set(games) != set(results):
        fail("Every original fixture needs exactly one verified final result")
    rows, stats = [], {"win": 0, "loss": 0, "push": 0, "unverified": 0}
    confidence_stats = {v: {"win": 0, "loss": 0, "push": 0} for v in ("LOW", "MEDIUM", "HIGH")}
    for id, game in games.items():
        result = results[id]
        if result.get("status") != "FINAL" or type(result.get("overtime_periods")) is not int or result["overtime_periods"] < 0:
            fail(f"Final game/OT confirmation missing: {id}")
        a = numeric(result.get("away_score"), "away final score")
        h = numeric(result.get("home_score"), "home final score")
        if int(a) != a or int(h) != h or min(a, h) < 0:
            fail(f"Non-integral basketball score: {id}")
        url(result.get("source_url"))
        score = int(a+h)
        if game["market_status"] != "PRETIP_MAIN_LINE_QUOTED":
            grade = "UNVERIFIED"
        elif score == game["market_line"]:
            grade = "PUSH"
        elif (score > game["market_line"]) == (game["selected_direction"] == "OVER"):
            grade = "WIN"
        else:
            grade = "LOSS"
        stats[grade.lower()] += 1
        if grade in {"WIN", "LOSS", "PUSH"}:
            confidence = game.get("analyst_confidence")
            if confidence not in confidence_stats:
                fail("Invalid qualitative confidence in the locked overlay")
            confidence_stats[confidence][grade.lower()] += 1
        rows.append({"away": game["away"], "home": game["home"], "official_total_including_ot": score,
                     "overtime_periods": result["overtime_periods"], "final_source_url": result["source_url"],
                     "locked_line": game["market_line"], "locked_direction": game["selected_direction"],
                     "model_raw_direction": game.get("raw_direction"),
                     "qualitative_confidence": game.get("analyst_confidence"),
                     "grade": grade})
    settled = stats["win"]+stats["loss"]
    for v, counts in confidence_stats.items():
        n = counts["win"] + counts["loss"]
        counts["accuracy_excluding_push"] = counts["win"] / n if n else None
    return {
        "schema_version": "nba-ou-shadow-retro-v2", "status": "POSTGAME_RETROSPECTIVE",
        "nba_local_date": overlay["nba_local_date"], "summary": {
            "selected_wins": stats["win"], "selected_losses": stats["loss"],
            "selected_pushes": stats["push"], "unverified": stats["unverified"],
            "qualitative_confidence_bins": confidence_stats,
            "selected_accuracy_excluding_push": stats["win"]/settled if settled else None,
            "selection_coverage": (stats["win"]+stats["loss"]+stats["push"])/len(games),
        }, "games": rows,
    }


def write_new_file(path: str, value: dict):
    p = Path(path)
    if p.exists():
        fail("Refusing to overwrite output (append-only protocol)")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Prospective NBA full-game main-line O/U shadow overlay")
    sub = p.add_subparsers(dest="operation", required=True)
    b = sub.add_parser("overlay")
    b.add_argument("--forecast", required=True)
    b.add_argument("--market", required=True)
    b.add_argument("--output", required=True)
    g = sub.add_parser("grade")
    g.add_argument("--overlay", required=True)
    g.add_argument("--finals", required=True)
    g.add_argument("--output", required=True)
    args = p.parse_args()
    if args.operation == "overlay":
        raw = Path(args.forecast).read_bytes()
        result = build_overlay(json.loads(raw), json.loads(Path(args.market).read_text(encoding="utf-8")), raw)
    else:
        result = grade_overlay(json.loads(Path(args.overlay).read_text(encoding="utf-8")),
                               json.loads(Path(args.finals).read_text(encoding="utf-8")))
    write_new_file(args.output, result)


if __name__ == "__main__":
    main()
