from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger

class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def obtener_titulo(self):
        logger.info("Obteniendo título de la página")
        titulo_elemento = self.wait.until(EC.visibility_of_element_located(self._TITLE))
        titulo = titulo_elemento.text
        logger.info(f"Título obtenido: {titulo}")
        return titulo

    def obtener_contador_carrito(self):
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            contador = int(badge.text)
            logger.info(f"Contador del carrito: {contador}")
            return contador
        except:
            logger.info("Carrito vacío (contador = 0)")
            return 0

    def agregar_producto_por_nombre(self, nombre_producto):
        logger.info(f"Buscando y agregando producto: {nombre_producto}")
        productos = self.driver.find_elements(*self._PRODUCTS)
        
        for producto in productos:
            try:
                nombre_elemento = producto.find_element(By.CLASS_NAME, "inventory_item_name")
                if nombre_elemento.text == nombre_producto:
                    boton_agregar = producto.find_element(By.TAG_NAME, "button")
                    boton_agregar.click()
                    logger.info(f"Producto '{nombre_producto}' agregado al carrito")
                    return True
            except Exception as e:
                continue
        
        logger.error(f"No se encontró el producto: {nombre_producto}")
        raise Exception(f"No se encontró el producto: {nombre_producto}")