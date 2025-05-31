# talentolab-automation-framework

Framework completo de testing que integra Pytest con Behave (BDD) para el proyecto final del curso.

## 🚀 Instalación y configuración

# Instalar dependencias

pip install -r requirements.txt

# Verificar instalación

pytest --version
behave --version

📋 Ejecutar tests
Solo BDD (Behave)

# Todos los scenarios

behave

# Solo smoke tests

behave -t @smoke

# Solo regression tests

behave -t @regression

# Con reportes HTML

behave -f html -o reports/behave.html

Solo Pytest

# Tests de integración BDD

pytest tests_behave/ -v

# Solo smoke

pytest -m smoke -v

# Tests lentos

pytest -m slow -v
Framework completo (Pytest + BDD)
bash# Ejecución unificada
pytest -v

# Con reporte HTML completo

pytest --html=reports/framework_report.html --self-contained-html
📁 Estructura del proyecto
talentolab_framework/
├── features/ # Features BDD en Gherkin
│ ├── steps/ # Step definitions
│ ├── login.feature # Scenarios de login
│ └── cart.feature # Scenarios de carrito
├── pages/ # Page Object Model
├── tests_behave/ # Integración Pytest + BDD
├── utils/ # Utilidades y logging
├── logs/ # Archivos de log
└── reports/ # Reportes HTML y capturas
🎯 Features implementadas
Login (login.feature)

✅ Login exitoso con credenciales válidas (@smoke)
✅ Login fallido con credenciales inválidas (@regression)
✅ Validación de campos vacíos (@regression)

Carrito (cart.feature)

✅ Agregar producto al carrito (@smoke)
✅ Agregar múltiples productos (@regression)
✅ Persistencia del carrito entre páginas

📊 Reportes generados

Pytest HTML: reports/pytest_report.html
Behave HTML: reports/behave.html
Behave JSON: reports/behave.json
Logs detallados: logs/bdd_suite.log
Screenshots: reports/screens/ (en fallos)

🔧 Comandos útiles
bash# Ejecutar solo login scenarios
behave -t @smoke features/login.feature

# Ejecutar solo cart scenarios

behave features/cart.feature

# Debug mode con salida detallada

behave -v -s

# Generar reportes múltiples

behave -f json -o reports/behave.json -f html -o reports/behave.html -f pretty
🎭 Tags disponibles

@smoke: Tests críticos y rápidos
@regression: Suite completa de regresión
@ui: Tests de interfaz de usuario
@wip: Work in progress (excluidos por defecto)

🔗 Integración con el proyecto final
Este framework forma parte del proyecto final del curso y demuestra:

✅ BDD con Gherkin legible para stakeholders
✅ Integración Pytest + Behave
✅ Page Object Model reutilizable
✅ Reportes HTML profesionales
✅ Logging centralizado y capturas automáticas
✅ Preparación para CI/CD

Para talentolab_framework:
bashcd talentolab_framework

# Instalar dependencias

pip install -r requirements.txt

# Ejecutar framework completo

pytest -v

# Solo BDD smoke

behave -t @smoke

# Solo BDD regression

behave -t @regression

# Reportes completos

behave -f html -o reports/behave.html -f json -o reports/behave.json

![CI Status](https://github.com/emilianospinoso/talentolab-automation-framework/actions/workflows/ci.yml/badge.svg)
