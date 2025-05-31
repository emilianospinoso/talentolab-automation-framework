from behave import given, when, then, step
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger
from selenium.webdriver.common.by import By

@given('que estoy logueado en SauceDemo con usuario "{usuario}"')
def step_login_previo(context, usuario):
    """Realiza login previo para tests de carrito"""
    logger.info(f"BDD: Realizando login previo con usuario: {usuario}")
    context.login_page = LoginPage(context.driver)
    context.login_page.abrir()
    context.login_page.login_completo(usuario, "secret_sauce")
    
    # Verificar que el login fue exitoso
    assert "inventory.html" in context.driver.current_url

@given('estoy en la página de inventario')
def step_en_inventario(context):
    """Verifica que está en la página de inventario"""
    logger.info("BDD: Verificando que estoy en inventario")
    context.inventory_page = InventoryPage(context.driver)
    titulo = context.inventory_page.obtener_titulo()
    assert titulo == "Products", f"No estoy en inventario. Título: {titulo}"

@given('que el carrito está vacío')
def step_carrito_vacio(context):
    """Verifica que el carrito esté vacío"""
    logger.info("BDD: Verificando que el carrito está vacío")
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    
    contador = context.inventory_page.obtener_contador_carrito()
    assert contador == 0, f"El carrito no está vacío. Contador: {contador}"

@given('que he agregado "{producto}" al carrito')
def step_producto_agregado_previo(context, producto):
    """Agrega un producto al carrito como precondición"""
    logger.info(f"BDD: Agregando {producto} al carrito como precondición")
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    
    context.inventory_page.agregar_producto_por_nombre(producto)

@when('agrego el producto "{producto}" al carrito')
def step_agregar_producto(context, producto):
    """Agrega un producto específico al carrito"""
    logger.info(f"BDD: Agregando producto al carrito: {producto}")
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    
    # Guardar contador inicial
    context.contador_inicial = context.inventory_page.obtener_contador_carrito()
    
    # Agregar producto
    context.inventory_page.agregar_producto_por_nombre(producto)

@when('agrego los siguientes productos al carrito')
def step_agregar_multiples_productos(context):
    """Agrega múltiples productos al carrito"""
    logger.info("BDD: Agregando múltiples productos al carrito")
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    
    context.contador_inicial = context.inventory_page.obtener_contador_carrito()
    context.productos_agregados = 0
    
    for row in context.table:
        # Obtener el nombre del producto de la primera columna
        producto = list(row.cells)[0]
        logger.info(f"Agregando: {producto}")
        context.inventory_page.agregar_producto_por_nombre(producto)
        context.productos_agregados += 1

@when('navego a otra sección y vuelvo al inventario')
def step_navegar_y_volver(context):
    """Simula navegación entre páginas"""
    logger.info("BDD: Navegando a otra sección y volviendo")
    # En SauceDemo podemos ir al carrito y volver
    context.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    context.driver.find_element(By.ID, "continue-shopping").click()

@then('el contador del carrito debería mostrar "{contador_esperado}"')
def step_verificar_contador(context, contador_esperado):
    """Verifica el contador del carrito"""
    logger.info(f"BDD: Verificando contador del carrito: {contador_esperado}")
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    
    contador_actual = context.inventory_page.obtener_contador_carrito()
    contador_esperado = int(contador_esperado)
    
    assert contador_actual == contador_esperado, \
        f"Contador incorrecto. Esperado: {contador_esperado}, Actual: {contador_actual}"

@then('el botón del producto debería cambiar a "Remove"')
def step_verificar_boton_remove(context):
    """Verifica que el botón cambió a Remove"""
    logger.info("BDD: Verificando que el botón cambió a Remove")
    # Buscar botón que contenga "remove" en su data-test
    remove_buttons = context.driver.find_elements(By.CSS_SELECTOR, "button[data-test*='remove']")
    assert len(remove_buttons) > 0, "No se encontraron botones Remove"