\# SentinelShield Controlled Test Plan



\## Scope and authorization



All tests are performed only against the locally hosted SentinelShield lab application or a private, authorized virtual lab. No external systems are tested.



\## Test environment



| Item | Value |

|---|---|

| Operating system | Windows |

| Application framework | Flask |

| Local application URL | `http://127.0.0.1:5000` |

| Test client | Browser, PowerShell |

| Security-event log | `logs/events.jsonl` |



\## Controlled test cases



| ID | Test type | Expected result | Detection rule / status | Observed result |

|---|---|---|---|---|

| TC-01 | Normal search request | Allowed, HTTP 200 | No rule | |

| TC-02 | Normal contact-form POST | Allowed, HTTP 201 | No rule | |

| TC-03 | SQL injection indicator | Blocked, HTTP 403 | `SQLI-001` | |

| TC-04 | XSS indicator | Blocked, HTTP 403 | `XSS-001` | |

| TC-05 | Directory-traversal indicator | Blocked, HTTP 403 | `PATH-001` | |

| TC-06 | Command-injection indicator in POST body | Blocked, HTTP 403 | `CMDI-001` | |

| TC-07 | Six requests from one IP within 60 seconds | Sixth request blocked, HTTP 429 | `RATE-001` | |

| TC-08 | Dashboard request | Dashboard loads, HTTP 200 | N/A | |

| TC-09 | Automated test suite | All tests pass | N/A | |



\## Test evidence



For each completed test, record:



\- Date and time

\- Request type and endpoint

\- Expected HTTP status

\- Actual HTTP status

\- Rule ID and category from `logs/events.jsonl`

\- Screenshot filename

\- Any unexpected behavior



\## Automated testing



Run the test suite with:



```powershell

python -m unittest discover -s tests -v

```



\## Accuracy and limitations



A passing automated test suite proves that known controlled cases behave as expected. It does not prove that the WAF detects every real-world attack.



Use a labeled test dataset to calculate:



```text

Detection rate = True Positives / (True Positives + False Negatives) × 100

Example: you test 10 known malicious requests in your private lab. SentinelShield blocks 8 and allows 2.
TP = 8
FN = 2
Detection rate = 8 / (8 + 2) × 100 = 80%

False-positive rate = False Positives / (False Positives + True Negatives) × 100

Then you test 20 harmless requests. It allows 18 but blocks 2 by mistake.
TN = 18
FP = 2
False-positive rate = 2 / (2 + 18) × 100 = 10%

```



Potential false positives can occur because SentinelShield uses simplified signature matching. Potential false negatives can occur when malicious requests do not resemble an existing rule or in other words when hacker use diffrent method that is not match in WAF rule.



\## Conclusion



SentinelShield demonstrated the workflow of request inspection, signature matching, rate limiting, HTTP blocking, structured security logging, and dashboard-based event analysis.

