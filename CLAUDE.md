## Constraints
- Never read .env files or any files with secrets
- Do not output environment variable values in responses
- Do not log or transmit API keys, tokens, or passwords
## AQA Lead Project
Resume repository

## Tech Stack
- Language: Python 
- Test framework: pytest
- UI tests: Playwright 
- API tests: requests, Pydantic
- CI: GitHub Actions
- ORM: SQLAlchemy 
- Monitoring/metrics: Datadog (datadog-api-client)

## Tools
- OS: MacOS
- IDE: PyCharm
- Package manager: UV

## Project Structure
automatedtests/
├── configs/
│   └── <environ>_cfg/
│       └── <environ>_common_cfg.json   # URL configs per environment
├── data/
│   └── test_data.py                    # test data (negative cases etc.)
├── db/
│   ├── connection.py                   # SQLAlchemy engine and session factory (MySQL+pymysql)
│   ├── models.py                       # ORM table models (User etc.)
│   └── queries.py                      # DB query functions (get_user_by_id etc.)
├── integrations/
│   └── datadog.py                      # sends events to Datadog
├── pages/
│   ├── base.py                         # BasePage — navigation, page properties
│   ├── element.py                      # Element — wrapper over Playwright Locator
│   ├── settings.py                     # URLs, Settings (Pydantic)
│   ├── api/
│   │   ├── api_registry.py             # endpoint registry
│   │   ├── http_client.py              # API class and HttpMethod
│   │   └── respons_models/
│   │       └── <entity>_models.py      # Pydantic models for API responses
│   ├── blocks/
│   │   ├── common_page_block.py        # header / footer — shared blocks for all pages
│   │   ├── login_page_blocks.py        # login page blocks
│   │   └── main_page_blocks.py         # main page blocks
│   └── pages/
│       ├── common_page.py              # CommonPage — connects BasePage with URLs
│       ├── login_page.py               # LoginPage
│       ├── main_page.py                # MainPage — QA Playground main page
│       └── study_tracker_page.py       # StudyTrackerPage — Study Tracker dashboard
└── tests/
    ├── ui/
    │   ├── test_login_page.py
    │   └── test_main_page.py
    ├── api/
    │   └── test_checking_acct_details.py
    └── db/
        └── test_db.py                  # SQLAlchemy DB query tests
conftest.py         # pytest fixtures: browser, page, page objects
pyproject.toml      # dependencies and pytest configuration

## Page Class Hierarchy                                                                                                     
  BasePage → CommonPage → CommonPageBlocks → <PageName>                                                                           
                                           └── <PageName>Blocks 

##  Conventions
- Test names: test_<action>_<expected_result>
- Fixtures in conftest.py
- UI tests use Page Object Model: page interaction logic is encapsulated in pages/
- API responses are validated via Pydantic models from models/
- pytest markers:
  - @pytest.mark.smoke    — critical checks, run first
  - @pytest.mark.ui       — all UI tests (Playwright)
  - @pytest.mark.api      — all API tests (requests)
  - @pytest.mark.regression — full regression suite
  - Code must be documented in English

## API Tests

### api_registry
Endpoint registry. Key — `'<entity>:<http_method>'`, fields: `endpoint`, `method`, `model`, `request_model`.

### API class (http_client.py)
`make_request(url, registry_key)` — method is taken from the registry automatically. Built-in status, request/response body validation and retry (3 attempts on 429, 500–504).

### HttpMethod
`str` enum. Raises an error with a list of allowed methods on invalid value.

### Pydantic models
`pages/api/respons_models/<entity>_models.py`. Requires package `pydantic[email]`.

## DB Tests

### connection.py
`get_engine()` — lazy initialization of SQLAlchemy engine (MySQL+pymysql, env vars `LPS_DB_*`).
`get_session_factory()` — lazy initialization of the session factory.

### models.py
ORM models based on `DeclarativeBase`. Current models: `User` (table `user`).

### queries.py
Query functions: accept `Session`, return an ORM object or `None`.
Example: `get_user_by_id(session, user_id)`.

### Fixture
`db_session` in `conftest.py` — provides an SQLAlchemy session for each test.

## Integrations

### datadog.py (`integrations/datadog.py`)
`send_event_to_datadog(title, text, extra_tags)` — sends an event to Datadog via `datadog-api-client`.
Tag `run_id:<unix_ts>` is automatically added to each event for grouping by run.
Configuration is read from environment variables (`DD_API_KEY`, `DD_APP_KEY`).

## Goals
Publish to GitHub as a demo test automation project and code sample for an AQA Lead resume.

 ## File Handling Rules                                                                                                     
  - Never modify files without explicit user permission                                                                   
  - Before any file change — ask for confirmation                                                                           
  - Reading files is allowed without permission                                                                             
  - Propose changes as text in chat, do not apply them independently