import time
import os
from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv('SITE')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def marcar_asistencia():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Cambia a False si quieres ver lo que hace
        # Bloquear permisos de geolocalización
        context = browser.new_context(
            permissions=[],  # No se otorgan permisos
            geolocation=None,  # Se bloquea ubicación
        )

        page = context.new_page()

        # 1. Ir a la página de login
        page.goto(f"{ODOO_URL}/web/login")
        print("Loading Site to Log In...")

        # 2. Completar formulario y enviar
        page.fill('input[name="login"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('text=Log in')

        # 3. Esperar a que cargue la interfaz principal
        print("Logging In...")
        page.wait_for_url(f"{ODOO_URL}/web", timeout=15000)

        # 4. Esperar a que el systray esté disponible y hacer click en botón de asistencia
        page.wait_for_selector('i.fa-circle', timeout=10000)

        # Hacer click en el botón de check-in/check-out
        page.click('i.fa-circle')

        try:
            page.wait_for_selector('.btn-success', timeout=5000)
            page.locator('.btn-success').click()
            print("🟢 Succesfull Check-In")
        except TimeoutError:
            page.wait_for_selector('.btn-warning', timeout=5000)
            page.locator('.btn-warning').click()
            print("🔴 Successfull Check-Out")


        # Esperar que termine el proceso (puedes ajustar si da errores)
        time.sleep(2)

if __name__ == "__main__":
    try:
        marcar_asistencia()
    except Exception as e:
        print(f"Unexpected Error: {e}")