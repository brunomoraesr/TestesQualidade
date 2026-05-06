import math
import os
import time

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

_api_response_times: list[float] = []


# ── Configuração global ────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def config():
    return {
        "petstore_base_url": os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2"),
        "saucedemo_base_url": os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com"),
        "saucedemo_user": os.getenv("SAUCEDEMO_USER", "standard_user"),
        "saucedemo_password": os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce"),
        "browser": os.getenv("BROWSER", "chrome").lower(),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "implicit_wait": int(os.getenv("IMPLICIT_WAIT", "10")),
    }


# ── API ────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def api_session(config):
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    session.base_url = config["petstore_base_url"]
    session.hooks["response"].append(
        lambda r, *a, **kw: _api_response_times.append(r.elapsed.total_seconds() * 1000)
    )
    yield session
    session.close()


# ── Web / Selenium ─────────────────────────────────────────────────────────────

def _build_chrome_driver(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)


def _build_firefox_driver(headless: bool) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)


@pytest.fixture(scope="function")
def driver(config):
    browser  = config["browser"]
    headless = config["headless"]

    builders = {
        "chrome":  lambda: _build_chrome_driver(headless),
        "firefox": lambda: _build_firefox_driver(headless),
    }
    if browser not in builders:
        raise ValueError(f"Navegador não suportado: '{browser}'. Use 'chrome' ou 'firefox'.")

    drv = builders[browser]()
    yield drv
    drv.quit()


# ── Relatório HTML ─────────────────────────────────────────────────────────────

def pytest_configure(config):
    config._metadata = getattr(config, "_metadata", {})
    config._metadata["Projeto"] = "TestesQualidade"
    config._metadata["Módulos"] = "API (Petstore) | Web (SauceDemo)"


# ── Resumo estilo Newman no terminal ──────────────────────────────────────────

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats   = terminalreporter.stats
    passed  = len(stats.get("passed",  []))
    failed  = len(stats.get("failed",  []))
    error   = len(stats.get("error",   []))
    xfailed = len(stats.get("xfailed", []))
    xpassed = len(stats.get("xpassed", []))
    total   = passed + failed + error + xfailed + xpassed
    n_fail  = failed + error

    duration = time.time() - terminalreporter._sessionstarttime

    W, N = 20, 9
    # total line width: 1 + (W+2) + 1 + (N+2) + 1 + (N+2) + 1  = W + 2N + 10
    total_w = W + 2 * N + 10

    sep = f"+{'-' * (W + 2)}+{'-' * (N + 2)}+{'-' * (N + 2)}+"

    def row(label: str, executed: int, failed_n: int) -> str:
        return f"| {label:<{W}} | {executed:>{N}} | {failed_n:>{N}} |"

    def full_row(text: str) -> str:
        inner = total_w - 4  # remove leading `| ` and trailing ` |`
        return f"| {text:<{inner}} |"

    lines = [
        sep,
        f"| {'':>{W}} | {'executed':>{N}} | {'failed':>{N}} |",
        sep,
        row("iterations", 1,      int(n_fail > 0)),
        row("tests",      total,  n_fail),
        row("passed",     passed, 0),
    ]

    if xfailed:
        lines.append(row("xfailed", xfailed, 0))
    if xpassed:
        lines.append(row("xpassed", xpassed, 0))

    lines.append(sep)
    lines.append(full_row(f"total run duration: {duration:.1f}s"))

    if _api_response_times:
        n   = len(_api_response_times)
        avg = sum(_api_response_times) / n
        mn  = min(_api_response_times)
        mx  = max(_api_response_times)
        sd  = math.sqrt(sum((t - avg) ** 2 for t in _api_response_times) / n)
        lines.append(full_row(
            f"requests: {n}  |  "
            f"avg: {avg:.0f}ms  [min: {mn:.0f}ms, max: {mx:.0f}ms, s.d.: {sd:.0f}ms]"
        ))

    lines.append(sep)

    terminalreporter.write_sep("=", "test run summary")
    for line in lines:
        terminalreporter.write_line(line)
