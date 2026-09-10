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

    def test_allows_normal_contact_message(self):
        response = self.client.post(
            "/contact",
            data={"message": "hello"}
        )

        self.assertEqual(response.status_code, 201)

    def test_blocks_command_indicator_in_post_body(self):
        response = self.client.post(
            "/contact",
            data={"message": "hello;whoami"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json()["rule_id"],
            "CMDI-001"
        )


if __name__ == "__main__":
    unittest.main()