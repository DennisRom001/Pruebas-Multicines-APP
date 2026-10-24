import base64
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def mobile_driver(request):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    
    # Conexión al dispositivo físico
    options.device_name = "RFGL10LA6YR" 
    options.udid = "RFGL10LA6YR"
    options.automation_name = "UiAutomator2"
    
    # Mantiene la sesión para no tener que aceptar permisos cada vez
    options.set_capability("appium:noReset", True)

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    # Inicia la grabación forzando el reinicio y ajustando la resolución por compatibilidad
    driver.start_recording_screen(
        forceRestart=True, 
        videoSize="1280x720"
    )

    yield driver

    # --- CIERRE DE PRUEBA Y GUARDADO DE EVIDENCIA ---
    test_name = request.node.name
    raw_video = driver.stop_recording_screen()
    
    # Esta línea está perfecta: 'wb' (write binary) + b64decode
    with open(f"{test_name}.mp4", "wb") as video_file:
        video_file.write(base64.b64decode(raw_video))

    driver.quit()