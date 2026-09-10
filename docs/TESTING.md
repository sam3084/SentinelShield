# SentinelShield Controlled Test Plan

## Scope and authorization

All tests are performed only against the locally hosted SentinelShield lab application or a private, authorized virtual lab. No external systems are tested.

## Test environment

| Item | Value |
|---|---|
| Operating system | Windows |
| Application framework | Flask |
| Local application URL | `http://127.0.0.1:5000` |
| Test client | Browser and PowerShell |
| Security-event log | `logs/events.jsonl` |

## Controlled test cases

| ID | Test type | Expected result | Rule/status | Observed result |
|---|---|---|---|---|
| TC-01 | Normal search request | Allowed, HTTP 200 | No rule | Record during test |
| TC-02 | Normal contact POST | Allowed, HTTP 201 | No rule | Record during test |
| TC-03 | SQL injection indicator | Blocked, HTTP 403 | `SQLI-001` | Record during test |
| TC-04 | XSS indicator | Blocked, HTTP 403 | `XSS-001` | Record during test |
| TC-05 | Directory-traversal indicator | Blocked, HTTP 403 | `PATH-001` | Record during test |
| TC-06 | Local-file-inclusion indicator | Blocked, HTTP 403 | `LFI-001` | Record during test |
| TC-07 | Command-injection indicator in POST body | Blocked, HTTP 403 | `CMDI-001` | Record during test |
| TC-08 | Six requests from one IP in 60 seconds | Sixth blocked, HTTP 429 | `RATE-001` | Record during test |
| TC-09 | Dashboard request | Dashboard loads, HTTP 200 | N/A | Record during test |
| TC-10 | Automated test suite | All tests pass | N/A | Record during test |

## Evidence to capture

For each completed test, record the date/time, request type, expected and actual HTTP status, rule ID/category, screenshot filename, and any unexpected behavior.

## Automated testing

```powershell
python -m unittest discover -s tests -v
```

## Accuracy and limitations

A passing test suite proves known controlled cases behave as expected; it does not prove that every real-world attack is detected.

```text
Detection rate = True Positives / (True Positives + False Negatives) × 100
False-positive rate = False Positives / (False Positives + True Negatives) × 100
```

Example: if 10 known malicious requests are tested and 8 are blocked:

```text
True Positives = 8
False Negatives = 2
Detection rate = 8 / (8 + 2) × 100 = 80%
```

If 20 harmless requests are tested and 2 are blocked incorrectly:

```text
True Negatives = 18
False Positives = 2
False-positive rate = 2 / (2 + 18) × 100 = 10%
```

Simplified signatures may create false positives and can miss malicious requests that do not resemble existing rules. Rate limiting should be evaluated separately from signature accuracy because it blocks high request volume rather than malicious content.

## Conclusion

SentinelShield demonstrates request inspection, signature matching, rate limiting, HTTP blocking, structured security logging, and dashboard-based event analysis.
