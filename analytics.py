import json
from collections import Counter


def get_dashboard_summary(event_log):
    events = []

    if event_log.exists():
        with event_log.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    blocked_events = [
        event for event in events
        if event.get("decision") == "blocked"
    ]

    return {
        "total_requests": len(events),
        "allowed_requests": sum(
            event.get("decision") == "allowed"
            for event in events
        ),
        "blocked_requests": len(blocked_events),
        "category_counts": Counter(
            event.get("category", "unknown")
            for event in blocked_events
        ),
        "ip_counts": Counter(
            event.get("ip_address", "unknown")
            for event in blocked_events
        ),
        "recent_events": list(reversed(events[-10:])),
    }