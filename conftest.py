from typing import  Generator

import pytest


from _pytest.config.argparsing import Parser
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright, ViewportSize
from playwright_stealth import Stealth

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from automatedtests.db.connection import get_session_factory
from automatedtests.integrations.datadog import send_event_to_datadog
from automatedtests.pages.blocks.main_page_blocks import MainPageBlocks
from automatedtests.pages.blocks.login_page_blocks import LoginPageBlocks
from automatedtests.pages.settings import URLs, settings

from automatedtests.pages.pages.main_page import MainPage
from automatedtests.pages.pages.login_page import LoginPage
from automatedtests.pages.pages.study_tracker_page import StudyTrackerPage

load_dotenv()


def pytest_addoption(parser: Parser) -> None:
    """Registers CLI argument --environ for environment selection."""
    parser.addoption(
        "--environ",
        default="test",
        choices=["test", "staging", "prod"],
        help="Environment for test execution: test | staging | prod",
    )
    parser.addoption("--browser-name", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.addoption("--headless", default="true", choices=["true", "false"])
    parser.addoption("--slow-mo", default=0, type=int, help="Delay between actions (ms)")



@pytest.fixture(scope="session")
def urls(request) -> URLs:
    """Returns validated URLs for the given environment."""
    environ = request.config.getoption("--environ")
    return settings.load_urls(environ)


# ── Playwright (scope=session) ────────────────────────────────────────────────

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, request: pytest.FixtureRequest) -> Generator[Browser, None, None]:
    """Single browser for the entire session."""
    browser_name = request.config.getoption("--browser-name")
    headless = request.config.getoption("--headless") == "true"
    slow_mo = request.config.getoption("--slow-mo")

    browser = getattr(playwright_instance, browser_name).launch(
        headless=headless,
        slow_mo=slow_mo,
        args=["--disable-blink-features=AutomationControlled"],
    )
    yield browser
    browser.close()


# ── Context (scope=function) — isolation between tests ────────────────────────

@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """New context for each test: cookies, storage, auth — isolated."""
    ctx = browser.new_context(
        viewport=ViewportSize(width=1280, height=720),
        locale="ru-RU",
        timezone_id="Europe/Moscow",
        record_video_dir="reports/videos",   # None — if video is not needed
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.0.0 Safari/537.36"
        ),
    )
    ctx.set_default_timeout(10_000)
    yield ctx
    ctx.close()


# ── Page ──────────────────────────────────────────────────────────────────────

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Clean page for each test."""
    page = context.new_page()
    Stealth().apply_stealth_sync(page)
    yield page
    page.close()


# ── Authenticated context (optional) ──────────────────────────────────────────

@pytest.fixture
def auth_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Context with saved authentication state."""
    ctx = browser.new_context(
        storage_state="auth/state.json",   # saved once via playwright codegen
        viewport=ViewportSize(width=1280, height=720),
    )
    yield ctx
    ctx.close()

@pytest.fixture(scope="session")
def db_connectivity_check() -> None:
    """Checks DB availability once per session. If unavailable — sends alert to Datadog and skips tests."""
    try:
        session_factory = get_session_factory()
        with session_factory() as session:
            session.execute(text("SELECT 1"))
    except OperationalError as e:
        try:
            send_event_to_datadog(
                title="DB unavailable — tests skipped",
                text=str(e),
                extra_tags=["severity:critical", "suite:db"],
            )
        except Exception:
            pass
        pytest.skip("DB unavailable")


@pytest.fixture
def db_session(db_connectivity_check) -> Generator:
    """DB session with transaction rollback after each test."""
    session_factory = get_session_factory()
    session = session_factory()
    session.begin_nested()  # savepoint
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def main_page(page: Page, urls: URLs) -> MainPage:
    return MainPage(page, urls)

@pytest.fixture
def main_page_blocks(page: Page, urls: URLs) -> MainPageBlocks:
    return MainPageBlocks(page, urls)

@pytest.fixture
def login_page(page: Page, urls: URLs) -> LoginPage:
    return LoginPage(page, urls)

@pytest.fixture
def login_page_blocks(page: Page, urls: URLs) -> LoginPageBlocks:
    return LoginPageBlocks(page, urls)

@pytest.fixture
def study_tracker_page(page: Page, urls: URLs) -> StudyTrackerPage:
    return StudyTrackerPage(page, urls)

