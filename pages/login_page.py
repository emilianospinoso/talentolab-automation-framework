from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Selectores de SauceDemo
        self.campo_usuario = (By.ID, "user-name")
        self.campo_clave = (By.ID, "password")
        self.boton_login = (By.ID, "login-button")
        self.mensaje_error = (By.CSS_SELECTOR, "[data-test='error']")
        self.contenedor_error = (By.CLASS_NAME, "error-message-container")
        self.boton_cerrar_error = (By.CLASS_NAME, "error-button")
        
        # URL de SauceDemo
        self.url = "https://www.saucedemo.com/"
    
    def abrir(self):
        """Abre la página de login"""
        self.driver.get(self.url)
        # Esperar a que la página cargue completamente
        self.wait.until(EC.presence_of_element_located(self.campo_usuario))
        time.sleep(1)  # Pequeña pausa adicional para estabilidad
    
    def completar_usuario(self, usuario):
        """Completa el campo de usuario"""
        elemento = self.wait.until(EC.element_to_be_clickable(self.campo_usuario))
        elemento.clear()
        elemento.send_keys(usuario)
        time.sleep(0.5)  # Pausa para que se registre el input
    
    def completar_clave(self, clave):
        """Completa el campo de contraseña"""
        elemento = self.wait.until(EC.element_to_be_clickable(self.campo_clave))
        elemento.clear()
        elemento.send_keys(clave)
        time.sleep(0.5)  # Pausa para que se registre el input
    
    def hacer_clic_login(self):
        """Hace clic en el botón de login"""
        boton = self.wait.until(EC.element_to_be_clickable(self.boton_login))
        boton.click()
        time.sleep(2)  # Esperar a que se procese la petición
    
    def esta_error_visible(self):
        """Verifica si hay un mensaje de error visible"""
        try:
            # Intentar múltiples selectores para el error
            selectores_error = [
                (By.CSS_SELECTOR, "[data-test='error']"),
                (By.CLASS_NAME, "error-message-container"),
                (By.XPATH, "//*[contains(@class, 'error')]"),
                (By.XPATH, "//*[contains(text(), 'Epic sadface')]")
            ]
            
            for selector in selectores_error:
                try:
                    elemento = WebDriverWait(self.driver, 3).until(
                        EC.visibility_of_element_located(selector)
                    )
                    if elemento.is_displayed():
                        return True
                except TimeoutException:
                    continue
                except NoSuchElementException:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error verificando mensaje de error: {e}")
            return False
    
    def obtener_mensaje_error(self):
        """Obtiene el texto del mensaje de error"""
        try:
            # Intentar múltiples selectores
            selectores_error = [
                (By.CSS_SELECTOR, "[data-test='error']"),
                (By.CLASS_NAME, "error-message-container"),
                (By.XPATH, "//*[contains(@class, 'error')]")
            ]
            
            for selector in selectores_error:
                try:
                    elemento = WebDriverWait(self.driver, 3).until(
                        EC.visibility_of_element_located(selector)
                    )
                    texto = elemento.text.strip()
                    if texto:
                        return texto
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return ""
            
        except Exception as e:
            print(f"Error obteniendo mensaje de error: {e}")
            return ""
    
    def login_completo(self, usuario, clave):
        """Realiza el login completo"""
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
    
    def esta_en_pagina_login(self):
        """Verifica si está en la página de login"""
        try:
            return self.driver.current_url == self.url or "saucedemo.com" in self.driver.current_url
        except:
            return False
    
    def limpiar_errores(self):
        """Cierra mensajes de error si están presentes"""
        try:
            boton_cerrar = self.driver.find_element(*self.boton_cerrar_error)
            if boton_cerrar.is_displayed():
                boton_cerrar.click()
                time.sleep(0.5)
        except (NoSuchElementException, TimeoutException):
            pass  # No hay error para cerrar