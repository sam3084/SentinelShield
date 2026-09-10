import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from time import monotonic

from flask import Flask, jsonify, render_template, request

from waf_rules import inspect_request

app = Flask(__name__)

LOG_DIRECTORY = Path(__file__).parent / "logs"
LOG_DIRECTORY.mkdir(exist_ok=True)
EVENT_LOG = LOG_DIRECTORY / "events.jsonl"

RATE_LIMIT_MAX_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

request_history = defaultdict(deque)
request_history_lock = Lock()

RATE_LIMIT_RULE = {
    "id": "RATE-001",
    "category": "rate_limit",
}


def get_client_ip():
    return request.remote_addr or "unknown"


def is_rate_limited(client_ip):
    current_time = monotonic()
    cutoff_time = current_time - RATE_LIMIT_WINDOW_SECONDS

    with request_history_lock:
        history = request_history[client_ip]

        while history and history[0] <= cutoff_time:
            history.popleft()

        if len(history) >= RATE_LIMIT_MAX_REQUESTS:
            return True

        history.append(current_time)
        return False


def log_request_event(decision="allowed", rule=None):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip_address": get_client_ip(),
        "method": request.method,
        "path": request.path,
        "query_string": request.query_string.decode("utf-8", errors="replace"),
        "decision": decision,
        "rule_id": rule["id"] if rule else None,
        "category": rule["category"] if rule else None,
    }

    with EVENT_LOG.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(event) + "\n")


@app.before_request
def inspect_incoming_request():
    client_ip = get_client_ip()

    if is_rate_limited(client_ip):
        log_request_event(decision="blocked", rule=RATE_LIMIT_RULE)
        return jsonify(
            error="Too many requests",
            rule_id=RATE_LIMIT_RULE["id"]
        ), 429

    raw_query = request.query_string.decode("utf-8", errors="replace")
    raw_body = request.get_data(cache=True, as_text=True)

    matched_rule = inspect_request(
        request.path,
        raw_query,
        headers=dict(request.headers),
        body=raw_body,
    )

    if matched_rule:
        log_request_event(decision="blocked", rule=matched_rule)
        return jsonify(
            error="Request blocked by SentinelShield",
            rule_id=matched_rule["id"]
        ), 403

    log_request_event()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(
        service="SentinelShield",
        status="healthy"
    )


@app.post("/contact")
def contact():
    return jsonify(
        message="Contact message accepted for demonstration"
    ), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)