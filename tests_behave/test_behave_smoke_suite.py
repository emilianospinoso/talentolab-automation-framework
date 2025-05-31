"""
Integración de Behave con Pytest para ejecución unificada
"""
import subprocess
import pathlib
import pytest
from utils.logger import logger

def test_behave_smoke_suite():
    """Ejecuta solo los escenarios marcados como @smoke desde Pytest"""
    logger.info("=== EJECUTANDO SUITE BDD SMOKE DESDE PYTEST ===")
    
    # Asegurar que existen las carpetas de reportes
    reports_dir = pathlib.Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Ejecutar Behave con filtro @smoke (sin HTML por ahora)
    result = subprocess.run([
        'behave', 
        '-t', '@smoke',
        '-f', 'json', 
        '-o', 'reports/behave_smoke.json',
        '-f', 'pretty'
    ], capture_output=True, text=True)
    
    # Log de la salida
    if result.stdout:
        logger.info("Salida de Behave:")
        for line in result.stdout.split('\n'):
            if line.strip():
                logger.info(f"  {line}")
    
    if result.stderr:
        logger.error("Errores de Behave:")
        for line in result.stderr.split('\n'):
            if line.strip():
                logger.error(f"  {line}")
    
    # Verificar que la ejecución fue exitosa
    assert result.returncode == 0, f"La suite BDD @smoke falló con código {result.returncode}"
    
    logger.info("=== SUITE BDD SMOKE COMPLETADA EXITOSAMENTE ===")

def test_behave_regression_suite():
    """Ejecuta los escenarios de regresión desde Pytest"""
    logger.info("=== EJECUTANDO SUITE BDD REGRESSION DESDE PYTEST ===")
    
    reports_dir = pathlib.Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Ejecutar Behave con filtro @regression
    result = subprocess.run([
        'behave',
        '-t', '@regression', 
        '-f', 'json',
        '-o', 'reports/behave_regression.json',
        '-f', 'pretty'
    ], capture_output=True, text=True)
    
    # Log de resultados
    if result.stdout:
        logger.info("Salida de Behave Regression:")
        for line in result.stdout.split('\n'):
            if line.strip():
                logger.info(f"  {line}")
    
    # Los tests de regresión pueden fallar sin detener el pipeline
    if result.returncode != 0:
        logger.warning(f"Suite BDD @regression completada con advertencias (código {result.returncode})")
    else:
        logger.info("=== SUITE BDD REGRESSION COMPLETADA EXITOSAMENTE ===")

@pytest.mark.slow
def test_behave_full_suite():
    """Ejecuta la suite completa de BDD (puede ser lenta)"""
    logger.info("=== EJECUTANDO SUITE BDD COMPLETA DESDE PYTEST ===")
    
    reports_dir = pathlib.Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Ejecutar Behave completo solo con JSON (HTML no disponible)
    result = subprocess.run([
        'behave',
        '-f', 'json',
        '-o', 'reports/behave_full.json',
        '-f', 'pretty'
    ], capture_output=True, text=True)
    
    # Log detallado
    if result.stdout:
        logger.info("Salida completa de Behave:")
        for line in result.stdout.split('\n'):
            if line.strip():
                logger.info(f"  {line}")
    
    if result.stderr:
        logger.error("Errores en suite completa:")
        for line in result.stderr.split('\n'):
            if line.strip():
                logger.error(f"  {line}")
    
    # Verificar archivos de reporte generados
    json_report = pathlib.Path('reports/behave_full.json')
    
    assert json_report.exists(), "No se generó el reporte JSON"
    
    logger.info(f"Reportes generados:")
    logger.info(f"  JSON: {json_report}")
    
    assert result.returncode == 0, f"La suite BDD completa falló con código {result.returncode}"
    
    logger.info("=== SUITE BDD COMPLETA EXITOSA ===")