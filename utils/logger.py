import logging
import pathlib
from datetime import datetime

# Crear carpeta de logs si no existe
log_dir = pathlib.Path('logs')
log_dir.mkdir(exist_ok=True)

# Configuración del logger para BDD
logging.basicConfig(
    filename=log_dir / 'bdd_suite.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s – %(message)s',
    datefmt='%H:%M:%S',
    filemode='a'
)

# Logger específico para TalentoLab BDD
logger = logging.getLogger('talentolab_bdd')

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s [BDD] %(message)s', '%H:%M:%S')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

def log_session_start():
    logger.info("=" * 60)
    logger.info(f"NUEVA SESIÓN BDD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

def log_session_end():
    logger.info("=" * 60)
    logger.info("FIN DE SESIÓN BDD")
    logger.info("=" * 60)

def log_feature_summary(feature_name, scenarios_passed, scenarios_failed):
    logger.info(f"📊 RESUMEN - {feature_name}:")
    logger.info(f"   ✅ Pasaron: {scenarios_passed}")
    logger.info(f"   ❌ Fallaron: {scenarios_failed}")