import re
from urllib.parse import unquote_plus

RULES = [
    {
        "id": "SQLI-001",
        "category": "sql_injection",
        "description": "Boolean-based SQL injection indicator",
        "pattern": re.compile(
            r"\bor\s+\d+\s*=\s*\d+",
            re.IGNORECASE
        ),
    },

    {
        "id": "XSS-001",
        "category": "cross_site_scripting",
        "description": "Script-tag indicator",
        "pattern": re.compile(
            r"<\s*script\b",
            re.IGNORECASE
        ),
    },

    {
        "id": "PATH-001",
        "category": "directory_traversal",
        "description": "Parent-directory traversal indicator",
        "pattern": re.compile(
            r"\.\.[\\/]",
            re.IGNORECASE
        ),
    }
]


def inspect_request(path, raw_query_string):
    """Return the first matching WAF rule, or None when the request is safe."""
    request_data = unquote_plus(f"{path}?{raw_query_string}")

    for rule in RULES:
        if rule["pattern"].search(request_data):
            return rule

    return None