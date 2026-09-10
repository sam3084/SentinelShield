import json
import tempfile
import unittest
from pathlib import Path

from analytics import get_dashboard_summary


class TestDashboardAnalytics(unittest.TestCase):

    def test_calculates_security_event_summary(self):
        events = [
            {
                "ip_address": "192.0.2.10",
                "decision": "allowed",
                "path": "/",
            },
            {
                "ip_address": "192.0.2.10",
                "decision": "blocked",
                "category": "sql_injection",
            },
            {
                "ip_address": "192.0.2.10",
                "decision": "blocked",
                "category": "cross_site_scripting",
            },
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            event_log = Path(temporary_directory) / "events.jsonl"

            with event_log.open("w", encoding="utf-8") as log_file:
                for event in events:
                    log_file.write(json.dumps(event) + "\n")

            summary = get_dashboard_summary(event_log)

        self.assertEqual(summary["total_requests"], 3)
        self.assertEqual(summary["allowed_requests"], 1)
        self.assertEqual(summary["blocked_requests"], 2)
        self.assertEqual(summary["category_counts"]["sql_injection"], 1)
        self.assertEqual(
            summary["category_counts"]["cross_site_scripting"],
            1
        )
        self.assertEqual(summary["ip_counts"]["192.0.2.10"], 2)


if __name__ == "__main__":
    unittest.main()