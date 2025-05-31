from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger

class LoginPage:
    URL = "https://www.saucedemo.com/"
    
    _USER_INPUT = (By.ID, "user-name")
    _PASS_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def abrir(self):
        logger.info(f"Navegando a {self.URL}")
        self.driver.get(self.URL)
        return self
    
    def completar_usuario(self, usuario):
        logger.info(f"Completando usuario: {usuario}")
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self
    
    def completar_clave(self, clave):
        logger.info("Completando contraseña")
        campo = self.driver.find_element(*self._PASS_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self
    
    def hacer_clic_login(self):
        logger.info("Haciendo clic en botón de login")
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self
    
    def login_completo(self, usuario, clave):
        logger.info(f"Realizando login completo para usuario: {usuario}")
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
        return self
    
    def esta_error_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            logger.warning("Error de login visible")
            return True
        except:
            return False
    
    def obtener_mensaje_error(self):
        if self.esta_error_visible():
            mensaje = self.driver.find_element(*self._ERROR_MESSAGE).text
            logger.error(f"Mensaje de error: {mensaje}")
            return mensaje
        return ""