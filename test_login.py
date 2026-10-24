import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # <-- Agrega esta línea

def test_login_multicines(mobile_driver):
    # Configuramos una espera máxima de 15 segundos para los elementos
    wait = WebDriverWait(mobile_driver, 15)

    # 1. Ir a la pestaña "Perfil"
    # Usamos ACCESSIBILITY_ID que es el content-desc
    btn_perfil = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Perfil")))
    btn_perfil.click()

    # 2. Clic en el botón de Google
    btn_google = wait.until(EC.presence_of_element_located((
        AppiumBy.XPATH, 
        "(//android.widget.TextView[@text='Hola, ingresa con tu cuenta']/..//com.horcrux.svg.SvgView)[2]"
    )))
    btn_google.click()

    # 3. Seleccionar la cuenta de Google
    # Appium interactúa con los servicios nativos de Android. Buscamos por tu nombre.
    cuenta_google = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Dennis Romero')]")))
    cuenta_google.click()

    # 4. Seleccionar el cine más cercano Manejo del Pop-up opcional
    try:
        # Usamos un wait más corto (5 segundos) exclusivo para el pop-up
        # Por si el pop no aparece, no queremos que falle la prueba, solo lo ignoramos y seguimos con el flujo
        wait_popup = WebDriverWait(mobile_driver, 5)
        btn_cine = wait_popup.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@content-desc='Selecciona el cine más cercano' or @text='Selecciona el cine más cercano']")))
        btn_cine.click()
        print("\nPop-up de cine detectado y clickeado.")
    except TimeoutException:
        print("\nEl pop-up de cine no apareció. Continuando con el flujo...")

    # 5. Validación final: Comprobar que ingresamos correctamente
    # Usamos el motor nativo de Android (UiAutomator) y buscamos el nombre que aparece en la pantalla de bienvenida
    texto_bienvenida = wait.until(EC.presence_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR, 
        'new UiSelector().textContains("Dennis")'
    )))
    
    assert texto_bienvenida is not None
    print("¡Login exitoso validado!")