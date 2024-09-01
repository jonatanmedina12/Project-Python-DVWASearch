from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
class LoginGit:
    def __init__(self, password, user):
        self.password = password
        self.user = user

    def login_page(self):
        service = Service(ChromeDriverManager().install())
        options = ChromeOptions()
        driver = Chrome(service=service, options=options)
        # Aquí deberías añadir el código para navegar a la página de inicio de sesión de GitHub
        driver.get("https://github.com/login")
        # buscamos el campo login y password
        driver.find_element(By.ID,'login_field').send_keys(self.user)
        driver.find_element(By.ID,'password').send_keys(self.password)
        driver.find_element(By.NAME,'commit').click()

        #compramos si el login ha sido exitoso
        WebDriverWait(driver=driver,timeout=10).until(
            lambda  x : x.execute_script("return document.readyState == 'complete'")
        )
        err_msg = "Incorrect username or password"
        error = driver.find_elements(By.CLASS_NAME,"js-flash-alert")
        if any(err_msg in e.text for e in error):
            print("[!] el login no ha tenido exito")
            driver.close()
            return False
        else:
            print("[+] el login ha tenido exito. ")
            driver.close()
            return  True