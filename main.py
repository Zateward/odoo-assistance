import requests
from bs4 import BeautifulSoup

# Crear una sesión persistente
session = requests.Session()

# URL de login
url_login = "https://odoowebsite.dev.odoo.com/login"

# Headers para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": url_login,
}

# Searching for the CSRF token in the login form
response_get = session.get(url_login, headers=headers)
soup = BeautifulSoup(response_get.text, "html.parser")

csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
print("Token CSRF:", csrf_token)

login_payload = {
    "csrf_token": csrf_token,
    "login": "your username/email",  # Change this to your username or email
    "password": "your password",  # Change this to your password
    "redirect": "",  # This field is usually empty, but you can check the login form for its value
}

# Login to the website
response_login = session.post(url_login, headers=headers, data=login_payload)

if response_login.ok:
    print("✅ Successful login")
else:
    print("❌ Faithful login. Code:", response_login.status_code)
    print("Text:", response_login.text)

# Automating the attendance check-in/out
url_attendance = "https://odoowebsite.dev.odoo.com/hr_attendance/systray_check_in_out"

attendance_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://odoowebsite.dev.odoo.com",
    "Referer": "https://odoowebsite.dev.odoo.com/web",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "",
}

attendance_payload = {
    "id" : 0,
    "jsonrpc" : "2.0",
    "method" : "call",
    "params" : {}
}

response_attendance = session.post(url_attendance, headers=attendance_headers, json=attendance_payload)

try:
    result = response_attendance.json()
    state = result["result"]["attendance_state"]
    if state == "checked_in":
        print("🟢 Successful check-in")
    elif state == "checked_out":
        print("🔴 Successful check-out")
    else:
        print("⚠️ Unknown state:", state)
except Exception as e:
    print("❌ Error while registering attendance:", e)
    print(response_attendance.text)