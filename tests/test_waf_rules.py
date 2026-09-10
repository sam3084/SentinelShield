import unittest

from waf_rules import inspect_request


class TestWafRules(unittest.TestCase):

    def test_allows_normal_request(self):
        rule = inspect_request("/", "search=books")
        self.assertIsNone(rule)

    def test_detects_sql_injection_indicator(self):
        rule = inspect_request("/", "id=1%20OR%201=1")
        self.assertIsNotNone(rule)
        self.assertEqual(rule["id"], "SQLI-001")

    def test_detects_xss_indicator(self):
        rule = inspect_request(
            "/",
            "comment=%3Cscript%3Edemo%3C%2Fscript%3E"
        )
        self.assertIsNotNone(rule)
        self.assertEqual(rule["id"], "XSS-001")

    def test_detects_directory_traversal_indicator(self):
        rule = inspect_request(
            "/",
            "file=..%2F..%2Fexample.txt"
        )
        self.assertIsNotNone(rule)
        self.assertEqual(rule["id"], "PATH-001")

    def test_detects_local_file_inclusion_indicator(self):
        rule = inspect_request(
            "/",
            "file=%2Fetc%2Fpasswd"
        )
        self.assertIsNotNone(rule)
        self.assertEqual(rule["id"], "LFI-001")

    def test_detects_command_injection_indicator(self):
        rule = inspect_request(
            "/",
            "",
            body="message=hello%3Bwhoami"
        )
        self.assertIsNotNone(rule)
        self.assertEqual(rule["id"], "CMDI-001")


if __name__ == "__main__":
    unittest.main()
