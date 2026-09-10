import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from waf_rules import inspect_request

app = Flask(__name__)

LOG_DIRECTORY = Path(__file__).parent / "logs"
LOG_DIRECTORY.mkdir(exist_ok=True)
EVENT_LOG = LOG_DIRECTORY / "events.jsonl"


def get_client_ip():
    return request.remote_addr or "unknown"


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
    raw_query = request.query_string.decode("utf-8", errors="replace")
    matched_rule = inspect_request(request.path, raw_query)

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)