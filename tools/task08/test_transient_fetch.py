"""Transport-only bounded retry safety; deterministic, no network."""
import io
import ssl
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import independent_coverage_probe as source
import cloud_capture_candidate as capture


def response(body=b'{"events":[]}'):
    r = MagicMock()
    r.status = 200
    r.read.return_value = body
    r.__enter__.return_value = r
    return r


class SourceRetryTests(unittest.TestCase):
    URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=123"

    def test_transient_tls_alert_recovers_original_bytes(self):
        err=urllib.error.URLError(ssl.SSLError("tlsv1 alert internal error"))
        with patch.object(source.urllib.request,"urlopen",side_effect=[err,response(b"verified")]) as fetch, patch.object(source.time,"sleep") as sleep:
            self.assertEqual(source.get_bytes(self.URL),b"verified")
            self.assertEqual(fetch.call_count,2)
            sleep.assert_called_once_with(1.0)

    def test_exhausted_transient_tls_fails_closed(self):
        err=urllib.error.URLError(ssl.SSLError("tlsv1 alert internal error"))
        with patch.object(source.urllib.request,"urlopen",side_effect=err) as fetch, patch.object(source.time,"sleep") as sleep:
            with self.assertRaises(urllib.error.URLError):
                source.get_bytes(self.URL)
            self.assertEqual(fetch.call_count,4)
            self.assertEqual([x.args[0] for x in sleep.call_args_list],[1.0,2.0,4.0])

    def test_retry_http_429_then_success(self):
        err=urllib.error.HTTPError(self.URL,429,"Too Many Requests",{},None)
        with patch.object(source.urllib.request,"urlopen",side_effect=[err,response(b"ok")]) as fetch, patch.object(source.time,"sleep"):
            self.assertEqual(source.get_bytes(self.URL),b"ok")
            self.assertEqual(fetch.call_count,2)

    def test_no_retry_on_http_404(self):
        err=urllib.error.HTTPError(self.URL,404,"Not Found",{},None)
        with patch.object(source.urllib.request,"urlopen",side_effect=err) as fetch, patch.object(source.time,"sleep") as sleep:
            with self.assertRaises(urllib.error.HTTPError):
                source.get_bytes(self.URL)
            fetch.assert_called_once()
            sleep.assert_not_called()

    def test_no_retry_on_certificate_verification_failure(self):
        err=urllib.error.URLError(ssl.SSLCertVerificationError("certificate verify failed"))
        with patch.object(source.urllib.request,"urlopen",side_effect=err) as fetch, patch.object(source.time,"sleep") as sleep:
            with self.assertRaises(urllib.error.URLError):
                source.get_bytes(self.URL)
            fetch.assert_called_once()
            sleep.assert_not_called()

    def test_raw_capture_transient_tls_returns_original_bytes(self):
        err=urllib.error.URLError(ssl.SSLError("tlsv1 alert internal error"))
        with patch.object(capture.urllib.request,"urlopen",side_effect=[err,response(b"fresh csv")]) as fetch, patch.object(capture.time,"sleep") as sleep:
            body,code=capture.acquire(self.URL)
            self.assertEqual((body,code),(b"fresh csv",200))
            self.assertEqual(fetch.call_count,2)
            sleep.assert_called_once_with(1.0)

    def test_raw_capture_exhausted_failure_remains_fail_closed(self):
        err=urllib.error.URLError(ssl.SSLError("tlsv1 alert internal error"))
        with patch.object(capture.urllib.request,"urlopen",side_effect=err) as fetch, patch.object(capture.time,"sleep") as sleep:
            with self.assertRaises(urllib.error.URLError):
                capture.acquire(self.URL)
            self.assertEqual(fetch.call_count,4)
            self.assertEqual([x.args[0] for x in sleep.call_args_list],[1.0,2.0,4.0])

    def test_empty_response_fails_not_retried(self):
        with patch.object(source.urllib.request,"urlopen",return_value=response(b"")) as fetch, patch.object(source.time,"sleep") as sleep:
            with self.assertRaisesRegex(ValueError,"Empty upstream"):
                source.get_bytes(self.URL)
            fetch.assert_called_once()
            sleep.assert_not_called()


if __name__=="__main__":
    unittest.main()
