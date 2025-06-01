import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


API_ID = int(getenv("API_ID", "23287799")) #optional
API_HASH = getenv("API_HASH", "9f4f17dae2181ee22c275b9b40a3c907") #optional

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "7951600439").split()))
OWNER_ID = int(getenv("OWNER_ID", "7795212861"))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://dbzcommunity7:8aaNMFXxpvJceE3h@cluster0.bglvihu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
BOT_TOKEN = getenv("BOT_TOKEN", "8045371426:AAGjC5d5APxZJdAkGoue33tBir2IP91Q1fI")
ALIVE_PIC = getenv("ALIVE_PIC", 'https://files.catbox.moe/lchqg1.jpg')
ALIVE_TEXT = getenv("ALIVE_TEXT")
PM_LOGGER = getenv("PM_LOGGER")
LOG_GROUP = getenv("LOG_GROUP", "DBZ_LOG_GC")
GIT_TOKEN = getenv("GIT_TOKEN") #personal access token
REPO_URL = getenv("REPO_URL", "https://t.me/DBZ_ONGOING")
BRANCH = getenv("BRANCH", "master") #don't change
 
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")
