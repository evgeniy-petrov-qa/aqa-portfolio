# AQA Lead — Demo Test Suite

A demo test automation project for a resume.
Demonstrates an approach to test infrastructure organization: UI, API, DB, and monitoring.

## Stack

| Layer | Tool                         |
|-------|------------------------------|
| Language | Python 3.14              |
| Framework | pytest                   |
| UI tests | Playwright                |
| API tests | requests + Pydantic      |
| DB | SQLAlchemy + pymysql (MySQL) |
| Monitoring | Datadog                  |
| CI | GitHub Actions               |
| Packages | uv                        |

## Structure

```
automatedtests/
├── configs/        # URL configs per environment
├── data/           # test data
├── db/             # SQLAlchemy: engine, models, queries
├── integrations/   # Datadog
├── pages/          # Page Object Model
│   ├── api/        # HTTP client, endpoint registry, Pydantic models
│   ├── blocks/     # page blocks (header, login, etc.)
│   └── pages/      # pages (LoginPage, MainPage, etc.)
└── tests/
    ├── ui/         # Playwright tests
    ├── api/        # API tests
    └── db/         # SQLAlchemy test examples (skip — no real DB connection)
```

## Running

```bash
# install dependencies
uv sync

# install Playwright browsers
uv run playwright install

# all tests
uv run pytest

# smoke only
uv run pytest -m smoke

# UI only
uv run pytest -m ui
```

## Environment variables

Create a `.env` file in the project root:

```env
Copy `.env.example` to `.env` and fill in the variables
for https://qaplayground.com/
```

## Key design decisions

- **Page Object Model** with hierarchy `BasePage → CommonPage → Blocks → Page`
- **API client** with endpoint registry, Pydantic validation, and retry (429, 5xx)
- **DB layer** — SQLAlchemy organization example with savepoint fixture (transaction rollback after each test). Tests marked `@pytest.mark.skip`
- **Datadog integration** — example of sending alerts when infrastructure is unavailable
- **Claude Code** — project developed with an AI assistant; `CLAUDE.md` describes team conventions