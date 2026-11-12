"""VALIDATION-ONLY COMPATIBILITY MODULE — NOT THE FROZEN PREDICTION MODEL.

Extracts the exact team definitions and five data-validation/aggregation functions
from the previously SHA-verified frozen nba_baseline_v01.py (SHA-256 prefix b6efd52d).
No model fitting, inference coefficients, priors, or private parameters are here.
The original full 9-test suite also passed against the real frozen model locally.
Do not use this adapter for game predictions.
"""
import math
TEAMS = 'ATL BKN BOS CHA CHI CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN NOP NYK OKC ORL PHI PHX POR SAC SAS TOR UTA WAS'.split()
ALIASES = dict(NY='NYK', GS='GSW', NO='NOP', SA='SAS', UTAH='UTA', WSH='WAS')
FIELDS = dict(field_goals_made='field_goals_made', field_goal_attempts='field_goals_attempted',
              three_point_makes='three_point_field_goals_made', three_point_attempts='three_point_field_goals_attempted',
              free_throws_made='free_throws_made', free_throw_attempts='free_throws_attempted',
              offensive_rebounds='offensive_rebounds', turnovers='total_turnovers')

def norm(x):
    return ALIASES.get(x, x)


def validate_pair(rows):
    if len(rows) != 2 or rows[0]['team'] != rows[1]['opponent'] or rows[1]['team'] != rows[0]['opponent']:
        raise ValueError('Not two reciprocal team rows')
    for row, opp in (rows, rows[::-1]):
        for field in list(FIELDS) + ['points', 'opponent_points']:
            value = float(row[field])
            if value < 0 or not math.isfinite(value):
                raise ValueError('Invalid count')
        if float(row['points']) != float(opp['opponent_points']):
            raise ValueError('Conflicting scores')
        if float(row['points']) != 2*float(row['field_goals_made']) + float(row['three_point_makes']) + float(row['free_throws_made']):
            raise ValueError('Shooting does not sum to score')
        for made, attempted in [('field_goals_made', 'field_goal_attempts'), ('three_point_makes', 'three_point_attempts'), ('free_throws_made', 'free_throw_attempts')]:
            if float(row[made]) > float(row[attempted]):
                raise ValueError('Makes exceed attempts')


def empty():
    return dict(n=0, points=0., allowed=0., poss=0., minutes=0., or_sum=0., dr_sum=0., pace_sum=0.)


def update(state, game):
    p, mins = game['possessions'], game['minutes']
    for team, scored, allowed in [(game['home'], game['hp'], game['ap']), (game['away'], game['ap'], game['hp'])]:
        s = state.setdefault(team, empty())
        s['n'] += 1
        s['points'] += scored
        s['allowed'] += allowed
        s['poss'] += p
        s['minutes'] += mins
        s['or_sum'] += 100*scored/p
        s['dr_sum'] += 100*allowed/p
        s['pace_sum'] += p*48/mins


def rates(s):
    # HTML parity: arithmetic mean of game efficiencies and possessions/game.
    # Published "Pace" is NOT OT-normalized possessions per 48 minutes.
    return dict(n=s['n'], ortg=s['or_sum']/s['n'], drtg=s['dr_sum']/s['n'], pace=s['poss']/s['n'])
