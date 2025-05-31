from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Selectores de SauceDemo Inventory
        self.titulo_productos = (By.CLASS_NAME, "title")
        self.contador_carrito = (By.CLASS_NAME, "shopping_cart_badge")
        self.enlace_carrito = (By.CLASS_NAME, "shopping_cart_link")
        self.contenedor_inventario = (By.CLASS_NAME, "inventory_container")
        self.items_inventario = (By.CLASS_NAME, "inventory_item")
        
        # Patrones para botones
        self.patron_boton_add = "add-to-cart"
        self.patron_boton_remove = "remove"
    
    def obtener_titulo(self):
        """Obtiene el título de la página de inventario"""
        try:
            elemento = self.wait.until(EC.visibility_of_element_located(self.titulo_productos))
            return elemento.text.strip()
        except TimeoutException:
            return ""
    
    def obtener_contador_carrito(self):
        """Obtiene el número del contador del carrito"""
        try:
            # Esperar un momento para que se actualice el contador
            time.sleep(1)
            contador = self.driver.find_element(*self.contador_carrito)
            return int(contador.text)
        except (NoSuchElementException, ValueError):
            # Si no hay contador visible, significa que está en 0
            return 0
    
    def agregar_producto_por_nombre(self, nombre_producto):
        """Agrega un producto al carrito por su nombre"""
        try:
            # Normalizar nombre del producto para el selector
            nombre_normalizado = nombre_producto.lower().replace(' ', '-')
            
            # Selector específico para el botón de agregar de SauceDemo
            selector_boton = f"[data-test='add-to-cart-{nombre_normalizado}']"
            
            boton = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_boton)))
            boton.click()
            
            # Esperar a que se actualice la interfaz
            time.sleep(1)
            
            return True
            
        except TimeoutException:
            # Si el selector específico falla, intentar método alternativo
            return self._agregar_producto_alternativo(nombre_producto)
    
    def _agregar_producto_alternativo(self, nombre_producto):
        """Método alternativo para agregar producto"""
        try:
            # Buscar todos los items de inventario
            items = self.driver.find_elements(*self.items_inventario)
            
            for item in items:
                try:
                    # Buscar el nombre del producto en este item
                    nombre_elemento = item.find_element(By.CLASS_NAME, "inventory_item_name")
                    
                    if nombre_producto.lower() in nombre_elemento.text.lower():
                        # Encontrado el producto, buscar su botón Add to Cart
                        boton_add = item.find_element(By.CSS_SELECTOR, f"button[data-test*='{self.patron_boton_add}']")
                        
                        if boton_add.is_enabled():
                            boton_add.click()
                            time.sleep(1)
                            return True
                            
                except NoSuchElementException:
                    continue
            
            raise Exception(f"No se encontró el producto: {nombre_producto}")
            
        except Exception as e:
            print(f"Error agregando producto {nombre_producto}: {e}")
            return False
    
    def verificar_boton_remove_presente(self, nombre_producto):
        """Verifica si el botón Remove está presente para un producto"""
        try:
            nombre_normalizado = nombre_producto.lower().replace(' ', '-')
            selector_remove = f"[data-test='remove-{nombre_normalizado}']"
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_remove)))
            return True
            
        except TimeoutException:
            return False
    
    def ir_al_carrito(self):
        """Navega al carrito de compras"""
        try:
            enlace = self.wait.until(EC.element_to_be_clickable(self.enlace_carrito))
            enlace.click()
            time.sleep(1)
        except TimeoutException:
            raise Exception("No se pudo acceder al carrito")
    
    def esta_en_inventario(self):
        """Verifica si está en la página de inventario"""
        try:
            return "inventory.html" in self.driver.current_url
        except:
            return False
    
    def obtener_nombres_productos_disponibles(self):
        """Obtiene lista de nombres de productos disponibles"""
        try:
            nombres = []
            items = self.driver.find_elements(*self.items_inventario)
            
            for item in items:
                try:
                    nombre = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                    nombres.append(nombre)
                except NoSuchElementException:
                    continue
                    
            return nombres
            
        except Exception:
            return []
    
    def esperar_carga_completa(self):
        """Espera a que la página de inventario cargue completamente"""
        try:
            # Esperar el contenedor principal
            self.wait.until(EC.presence_of_element_located(self.contenedor_inventario))
            
            # Esperar a que haya al menos un producto
            self.wait.until(EC.presence_of_element_located(self.items_inventario))
            
            # Esperar el título
            self.wait.until(EC.visibility_of_element_located(self.titulo_productos))
            
            time.sleep(1)  # Pausa adicional para estabilidad
            
        except TimeoutException:
            raise Exception("La página de inventario no cargó correctamente")