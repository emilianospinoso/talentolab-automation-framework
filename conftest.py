import pytest
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.logger import logger

# Configuración para capturas de pantalla de Pytest
target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="function")
def driver():
    """Fixture de WebDriver para tests de Pytest (no BDD)"""
    logger.info("Configurando WebDriver para Pytest...")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    
    logger.info("WebDriver configurado para Pytest")
    
    yield driver
    
    logger.info("Cerrando WebDriver de Pytest...")
    driver.quit()

# Hook para capturas de pantalla en fallos de Pytest
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar pantallas en fallos de Pytest"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            file_name = target / f"pytest_{item.name}_{report.when}.png"
            
            try:
                driver.save_screenshot(str(file_name))
                logger.error(f"Screenshot Pytest guardado: {file_name}")
                
                if hasattr(report, 'extra'):
                    report.extra = getattr(report, 'extra', [])
                    report.extra.append({
                        'name': 'screenshot',
                        'format': 'image',
                        'content': str(file_name)
                    })
            except Exception as e:
                logger.error(f"Error al capturar pantalla en Pytest: {e}")

# Hooks de personalización del reporte HTML
def pytest_html_results_table_header(cells):
    """Personaliza el header del reporte HTML"""
    cells.insert(2, 'URL')
    cells.insert(3, 'Tipo')

def pytest_html_results_table_row(report, cells):
    """Personaliza las filas del reporte HTML"""
    cells.insert(2, getattr(report, 'page_url', '-'))
    
    # Identificar tipo de test
    if 'behave' in report.nodeid:
        test_type = 'BDD'
    elif hasattr(report, 'markers'):
        if 'api' in str(report.markers):
            test_type = 'API'
        elif 'ui' in str(report.markers):
            test_type = 'UI'
        else:
            test_type = 'Unit'
    else:
        test_type = 'Integration'
    
    cells.insert(3, test_type)

def pytest_sessionstart(session):
    """Se ejecuta al inicio de la sesión de Pytest"""
    logger.info("=== INICIANDO SESIÓN PYTEST + BDD ===")

def pytest_sessionfinish(session, exitstatus):
    """Se ejecuta al final de la sesión de Pytest"""
    logger.info(f"=== SESIÓN PYTEST FINALIZADA (exit: {exitstatus}) ===")