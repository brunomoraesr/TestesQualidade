import os

import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()


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
    """
    Sessão HTTP compartilhada por todos os testes de API.
    Escopo 'session' evita abrir/fechar conexão a cada teste.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    session.base_url = config["petstore_base_url"]
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
    # Selenium Manager (embutido no Selenium 4.6+) baixa o ChromeDriver correto
    # automaticamente — sem dependência de webdriver-manager.
    return webdriver.Chrome(options=options)


def _build_firefox_driver(headless: bool) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)


@pytest.fixture(scope="function")
def driver(config):
    """
    Instância do WebDriver criada para cada teste e encerrada ao final.
    Escopo 'function' garante isolamento total entre os testes.
    """
    browser = config["browser"]
    headless = config["headless"]

    builders = {
        "chrome": lambda: _build_chrome_driver(headless),
        "firefox": lambda: _build_firefox_driver(headless),
    }
    if browser not in builders:
        raise ValueError(f"Navegador não suportado: '{browser}'. Use 'chrome' ou 'firefox'.")

    drv = builders[browser]()
    # implicitly_wait omitido intencionalmente: misturar com WebDriverWait(explicit)
    # causa comportamento imprevisível em CI — cada poll interno do WebDriverWait
    # usa find_element(), que com implicit wait bloqueia 15 s por retry.
    # Todos os waits são explícitos via BasePage.
    yield drv
    drv.quit()


# ── Relatório HTML ─────────────────────────────────────────────────────────────

def pytest_configure(config):
    config._metadata = getattr(config, "_metadata", {})
    config._metadata["Projeto"] = "TestesQualidade"
    config._metadata["Módulos"] = "API (Petstore) | Web (SauceDemo)"
