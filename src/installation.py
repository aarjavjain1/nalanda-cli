import os
from getpass import getpass
import json

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    quit("Required Libraries aren't installed. Please restart installation.")

join = os.path.join

INSTALL_PATH = join(os.path.expanduser("~"), ".config/nalanda-cli")
SUBJECTS_FILE = join(INSTALL_PATH,"subjects.json")
DATA_FILE = join(INSTALL_PATH,"data.json")
CONFIG_FILE = join(INSTALL_PATH,"config.json")
LOGIN_LINK = "https://nalanda.bits-pilani.ac.in/login/index.php"
HOMEPAGE_LINK = "https://nalanda.bits-pilani.ac.in/my"

session = requests.session()

try:
    config = {}
    sub_name_url = {}
    URLS = {}

    while True:
        config["username"] = input("Enter BITS ID [Eg: f2016015]\n")
        config["username"] += "@pilani.bits-pilani.ac.in"

        config["password"] = getpass(prompt = "Enter nalanda password:\n",)

        result = session.post(LOGIN_LINK, data = config)
        result = BeautifulSoup(result.text, "html.parser")

        if not result.find_all("a", {"id": "loginerrormessage"}):
            break
        print("Username or Password Incorrect. Please retry")

    if not os.path.exists(INSTALL_PATH):
        os.makedirs(INSTALL_PATH)

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    result = session.get(HOMEPAGE_LINK)
    soup = BeautifulSoup(result.text, "html.parser")
    for x in soup.find_all("div", "column c1"):
        sub_name_url[x.contents[0].get("href")] = ((x.contents[0].contents[1]).split("/")[0]).split("\\")[0]
        URLS[x.contents[0].get("href")] = {
            "resource": [],
            "notice": [],
            "news":[]
        }

    json.dump(URLS, open(DATA_FILE, 'w'), indent=4)
    json.dump(sub_name_url, open(SUBJECTS_FILE, "w"), indent=4)
    print("Installation Successful ✔")

except KeyboardInterrupt:
    quit("Installation cancelled by user. Please retry.")
except requests.exceptions.ConnectionError:
    quit("No Internet Connection. Please retry.")
except IOError:
    quit("Unable to read from file. Please reinstall nalanda-cli.")
