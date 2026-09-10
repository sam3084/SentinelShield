\# SentinelShield



SentinelShield is a lightweight educational Web Application Firewall (WAF) and intrusion-detection project. It inspects incoming web requests, detects suspicious indicators, blocks matching requests, logs security events, applies IP-based rate limiting, and displays activity in a dashboard.



> This project is for controlled learning environments only. It is not a production WAF.



\## Project purpose



The purpose of SentinelShield is to demonstrate the security workflow:



```text

Request → Inspection → Detection decision → Blocking or allowing → Logging → Dashboard analysis

```



It helps explain how a simplified WAF can detect common web-attack indicators and traffic abuse.



\## Architecture



```mermaid

flowchart LR

&#x20;   A\[Browser or controlled lab client] --> B\[Flask application]

&#x20;   B --> C\[Rate limiter]

&#x20;   C --> D\[WAF rule engine]

&#x20;   D -->|Allowed| E\[Application endpoint]

&#x20;   D -->|Blocked| F\[HTTP 403 response]

&#x20;   C -->|Rate limit exceeded| G\[HTTP 429 response]

&#x20;   E --> H\[JSON event log]

&#x20;   F --> H

&#x20;   G --> H

&#x20;   H --> I\[Security dashboard]

```



\## Features



\- Request inspection before an endpoint processes the request

\- Inspection of URL paths, query strings, request headers, and POST bodies

\- Signature-based detection rules:

&#x20; - SQL injection indicator: `SQLI-001`

&#x20; - Cross-site scripting indicator: `XSS-001`

&#x20; - Directory traversal indicator: `PATH-001`

&#x20; - Command injection indicator: `CMDI-001`

\- IP-based rate limiting: `RATE-001`

\- Structured JSON Lines security logging

\- Dashboard showing request totals, blocked events, categories, IP activity, and recent events

\- Automated unit and integration tests



\## Project structure



```text

SentinelShield/

├── app.py                 # Flask application and WAF pipeline

├── waf\_rules.py           # Detection signatures and inspection function

├── analytics.py           # Log-summary calculations for the dashboard

├── templates/

│   ├── index.html         # Demonstration application page

│   └── dashboard.html     # Security-event dashboard

├── tests/                 # Automated tests

├── logs/                  # Runtime security events; not committed to Git

├── requirements.txt       # Python dependencies

└── README.md

```



\## Installation



```powershell

git clone <YOUR-REPOSITORY-URL>

cd SentinelShield

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt

```



\## Run the application



```powershell

python app.py

```



Open these local URLs:



\- Application: `http://127.0.0.1:5000`

\- Health check: `http://127.0.0.1:5000/health`

\- Security dashboard: `http://127.0.0.1:5000/dashboard`



\## Run automated tests



```powershell

python -m unittest discover -s tests -v

```



\## Security-event logging



Each request is recorded as one JSON object in `logs/events.jsonl`.



Important fields include:



| Field | Meaning |

|---|---|

| `timestamp` | Time recorded in UTC |

| `ip\_address` | Direct client IP address in this local lab |

| `method` | HTTP method, such as GET or POST |

| `path` | Requested endpoint |

| `query\_string` | URL query parameters |

| `decision` | `allowed` or `blocked` |

| `rule\_id` | Identifier of the matched detection rule |

| `category` | Detected threat category |



Request bodies and headers are inspected but are deliberately not written to logs, reducing the risk of storing sensitive data.



\## Important limitations



SentinelShield is a learning project. Its limitations include:



\- Signature matching cannot detect every attack variation.

\- Simple signatures can create false positives.

\- Rate-limit history is stored in memory and resets when the application restarts.

\- The application is intentionally bound to `127.0.0.1` for local-lab safety.

\- A production WAF would use stronger rule sets, proxy-aware IP handling, persistent/shared rate-limit storage, authentication, HTTPS, monitoring, and security hardening.



\## Future improvements



\- Add more carefully tested detection rules.

\- Store events in a database.

\- Use Redis for rate limiting across multiple application instances.

\- Add authentication for dashboard access.

\- Export dashboard reports.

\- Measure detection accuracy, false positives, and false negatives using a controlled test dataset.

