from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pathlib
from datetime import datetime
from utils.logger import logger, log_session_start, log_session_end

# Carpeta para capturas de pantalla
SCREEN_DIR = pathlib.Path('reports/screens')
SCREEN_DIR.mkdir(parents=True, exist_ok=True)

def before_all(context):
    """Se ejecuta una vez antes de todas las features"""
    log_session_start()
    logger.info("=== INICIANDO SUITE BDD TALENTOLAB ===")
    
    # Configurar Chrome para BDD
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    service = Service()
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.implicitly_wait(10)
    
    logger.info("WebDriver configurado para BDD")

def before_feature(context, feature):
    """Se ejecuta antes de cada feature"""
    logger.info(f"🎬 Iniciando Feature: {feature.name}")
    logger.info(f"Tags: {', '.join(feature.tags) if feature.tags else 'Sin tags'}")

def before_scenario(context, scenario):
    """Se ejecuta antes de cada scenario"""
    logger.info(f"▶️ Escenario: {scenario.name}")
    if scenario.tags:
        logger.info(f"   Tags: {', '.join(scenario.tags)}")

def before_step(context, step):
    """Se ejecuta antes de cada step"""
    logger.info(f"   📋 {step.step_type.capitalize()}: {step.name}")

def after_step(context, step):
    """Se ejecuta después de cada step"""
    if step.status == 'failed':
        logger.error(f"   ❌ STEP FALLÓ: {step.name}")
        
        # Capturar screenshot en caso de fallo
        if hasattr(context, 'driver'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            scenario_name = context.scenario.name.replace(' ', '_').replace('/', '_')
            step_name = step.name.replace(' ', '_').replace('/', '_')
            filename = f"FAIL_{scenario_name}_{step_name}_{timestamp}.png"
            filepath = SCREEN_DIR / filename
            
            try:
                context.driver.save_screenshot(str(filepath))
                logger.error(f"   📸 Screenshot guardado: {filepath}")
                
                # Adjuntar al contexto para reportes
                if not hasattr(context, 'screenshots'):
                    context.screenshots = []
                context.screenshots.append(str(filepath))
                
            except Exception as e:
                logger.error(f"   Error al guardar screenshot: {e}")
        
        # Log del error
        if hasattr(step, 'exception'):
            logger.error(f"   💥 Error: {step.exception}")
    else:
        logger.info(f"   ✅ {step.step_type.capitalize()}: {step.name}")

def after_scenario(context, scenario):
    """Se ejecuta después de cada scenario"""
    if scenario.status == 'failed':
        logger.error(f"❌ ESCENARIO FALLÓ: {scenario.name}")
        logger.error(f"   Duración: {scenario.duration:.2f}s")
    else:
        logger.info(f"✅ ESCENARIO EXITOSO: {scenario.name}")
        logger.info(f"   Duración: {scenario.duration:.2f}s")
    
    # Limpiar screenshots del contexto
    if hasattr(context, 'screenshots'):
        delattr(context, 'screenshots')

def after_feature(context, feature):
    """Se ejecuta después de cada feature"""
    passed = len([s for s in feature.scenarios if s.status == 'passed'])
    failed = len([s for s in feature.scenarios if s.status == 'failed'])
    
    logger.info(f"🎬 Feature completada: {feature.name}")
    logger.info(f"   Escenarios: {passed} ✅ | {failed} ❌")

def after_all(context):
    """Se ejecuta una vez después de todas las features"""
    if hasattr(context, 'driver'):
        context.driver.quit()
        logger.info("WebDriver cerrado")
    
    logger.info("=== SUITE BDD TALENTOLAB FINALIZADA ===")
    log_session_end()