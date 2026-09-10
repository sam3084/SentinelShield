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
    },
    {
        "id": "LFI-001",
        "category": "local_file_inclusion",
        "description": "Sensitive local-file inclusion indicator",
        "pattern": re.compile(
            r"(?:/etc/passwd|/proc/self/environ)",
            re.IGNORECASE
        ),
    },
    {
        "id": "CMDI-001",
        "category": "command_injection",
        "description": "Shell command chaining indicator",
        "pattern": re.compile(
            r"(?:;|\|\||&&)\s*(?:whoami|id|uname)\b",
            re.IGNORECASE
        ),
    },
]


def inspect_request(path, raw_query_string, headers=None, body=""):
    """Return the first matching WAF rule, or None for a safe request."""
    decoded_query = unquote_plus(raw_query_string)
    decoded_body = unquote_plus(body)

    header_text = ""
    if headers:
        header_text = "\n".join(
            f"{name}: {value}" for name, value in headers.items()
        )

    request_data = "\n".join([
        path,
        decoded_query,
        header_text,
        decoded_body,
    ])

    for rule in RULES:
        if rule["pattern"].search(request_data):
            return rule

    return None
