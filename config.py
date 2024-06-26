import os

API_ID = API_ID = 29321927

API_HASH = os.environ.get("API_HASH", "24bc15d8a4355268b4e412bacacf4a1b")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7203418230:AAF0uzrw8dF7n6zr-kB1NJdQhqB7xwKshvA")

PASS_DB = int(os.environ.get("PASS_DB", "721"))

OWNER = int(os.environ.get("OWNER", 6940485320))

LOG = -1002150280450

try:
  GROUPS =[]
  for x in (os.environ.get('GROUPS', '-1002032524765 -1002150280450').split()):
    GROUPS.append(int(x))
except ValueError:
    raise Exception("Your AUTH GROUPS list does not contain valid integers.")    

try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "5890553267").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER)


