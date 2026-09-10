import unittest

import app as sentinelshield


class TestSentinelShieldApp(unittest.TestCase):

    def setUp(self):
        sentinelshield.app.config["TESTING"] = True
        sentinelshield.request_history.clear()
        self.client = sentinelshield.app.test_client()

    def test_rate_limit_blocks_sixth_request(self):
        for _ in range(5):
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 200)

        blocked_response = self.client.get("/health")

        self.assertEqual(blocked_response.status_code, 429)
        self.assertEqual(
            blocked_response.get_json()["rule_id"],
            "RATE-001"
        )


if __name__ == "__main__":
    unittest.main()