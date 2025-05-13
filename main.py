import time
import os
from playwright.sync_api import sync_playwright
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
        print("🔐 Cargando login...")

        # 2. Completar formulario y enviar
        page.fill('input[name="login"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('text=Log in')

        # 3. Esperar a que cargue la interfaz principal
        print("🔓 Iniciando sesión...")
        page.wait_for_url(f"{ODOO_URL}/web", timeout=15000)

        # 4. Esperar a que el systray esté disponible y hacer click en botón de asistencia
        page.wait_for_selector('i.fa-circle', timeout=10000)
        print("👀 Botón de asistencia detectado.")

        # Hacer click en el botón de check-in/check-out
        page.click('i.fa-circle')
        
        # Si existe .btn-success hacer click en el y si no hacer click en .btn-warning
        if page.locator('.btn-success').is_visible():
            page.click('.btn-success')
        else:
            page.click('.btn-warning')

        # Esperar que termine el proceso (puedes ajustar si da errores)
        time.sleep(2)

        print("✅ Asistencia marcada correctamente.")
        browser.close()

if __name__ == "__main__":
    marcar_asistencia()
