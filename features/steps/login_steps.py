from behave import given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger

@given('que abro la página de login de SauceDemo')
def step_abrir_login(context):
    """Abre la página de login"""
    logger.info("BDD: Abriendo página de login")
    context.login_page = LoginPage(context.driver)
    context.login_page.abrir()

@when('ingreso el usuario "{usuario}" y la contraseña "{password}"')
def step_ingresar_credenciales(context, usuario, password):
    """Ingresa usuario y contraseña"""
    logger.info(f"BDD: Ingresando credenciales - Usuario: {usuario}")
    context.login_page.completar_usuario(usuario)
    context.login_page.completar_clave(password)

@when('hago clic en el botón de login')
def step_click_login(context):
    """Hace clic en el botón de login"""
    logger.info("BDD: Haciendo clic en botón de login")
    context.login_page.hacer_clic_login()

@when('dejo los campos de usuario y contraseña vacíos')
def step_campos_vacios(context):
    """Deja los campos vacíos"""
    logger.info("BDD: Dejando campos vacíos")
    # Los campos ya están vacíos por defecto

@then('debería ser redirigido a la página de inventario')
def step_verificar_redireccion(context):
    """Verifica redirección al inventario"""
    logger.info("BDD: Verificando redirección a inventario")
    assert "inventory.html" in context.driver.current_url, \
        f"No se redirigió al inventario. URL actual: {context.driver.current_url}"

@then('debería ver el título "{titulo_esperado}"')
def step_verificar_titulo(context, titulo_esperado):
    """Verifica el título de la página"""
    logger.info(f"BDD: Verificando título: {titulo_esperado}")
    context.inventory_page = InventoryPage(context.driver)
    titulo_actual = context.inventory_page.obtener_titulo()
    assert titulo_actual == titulo_esperado, \
        f"Título incorrecto. Esperado: {titulo_esperado}, Actual: {titulo_actual}"

@then('debería ver un mensaje de error')
def step_verificar_error(context):
    """Verifica que aparezca un mensaje de error"""
    logger.info("BDD: Verificando mensaje de error")
    assert context.login_page.esta_error_visible(), \
        "No se mostró mensaje de error cuando debería"

@then('debería ver un mensaje de error indicando campos requeridos')
def step_verificar_error_campos_requeridos(context):
    """Verifica error específico de campos requeridos"""
    logger.info("BDD: Verificando error de campos requeridos")
    assert context.login_page.esta_error_visible(), \
        "No se mostró mensaje de error para campos requeridos"
    mensaje = context.login_page.obtener_mensaje_error()
    assert len(mensaje) > 0, "El mensaje de error está vacío"

@then('debería permanecer en la página de login')
def step_verificar_permanencia_login(context):
    """Verifica que sigue en la página de login"""
    logger.info("BDD: Verificando permanencia en login")
    assert "inventory.html" not in context.driver.current_url, \
        "No debería haber sido redirigido al inventario"