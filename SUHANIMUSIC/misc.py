import socket
import time

import heroku3
from pyrogram import filters

import config
from SUHANIMUSIC.core.mongo import mongodb

from .logging import LOGGER

SUDOERS = filters.user()

SUBSCRIBERS = filters.user()
IGNORED = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘 𝗟𝗢𝗔𝗗 𝗕𝗔𝗕𝗬🍫........")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info(f"𝗦𝗨𝗗𝗢 𝗨𝗦𝗘𝗥 𝗗𝗢𝗡𝗘✨🎋.")


async def ignore():
    global IGNORED
    ignoredb = mongodb.ignorelist  # Reference your MongoDB collection
    ignorelist = await ignoredb.find().to_list(length=None)  # Fetch all documents
    
    # Iterate through each document and extract the `user_id`
    for document in ignorelist:
        user_id = document.get("user_id")  # Get the user_id field
        if user_id:  # Ensure user_id exists and is valid
            IGNORED.add(user_id)  # Add the user_id to the IGNORED filter

    LOGGER(__name__).info(f"IGNORED users loaded: {[doc['user_id'] for doc in ignorelist]}")

async def update_subscriber_ids():
    global SUBSCRIBERS
    # Replace 'subscribersdb' with your actual MongoDB collection reference for subscribers
    subscribersdb = mongodb.subscribers
    subscribers = await subscribersdb.find().to_list(length=None)  # Fetch all subscribers
    SUBSCRIBERS = {sub["user_id"] for sub in subscribers}  # Extract user IDs into a set

    LOGGER(__name__).info(f"Subscriber IDs updated")

def heroku():
    global HAPP
    if is_heroku:
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"🍟𝗛𝗘𝗥𝗢𝗞𝗨 𝗔𝗣𝗣 𝗡𝗔𝗠𝗘 𝗟𝗢𝗔𝗗......💦")
            except BaseException:
                LOGGER(__name__).warning(
                    f"✨𝐘𝐨𝐮 𝐇𝐚𝐯𝐞 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝 𝐇𝐞𝐫𝐨𝐤𝐮 𝐀𝐩𝐢 𝐊𝐞𝐲 𝐀𝐧𝐝 𝐇𝐞𝐫𝐨𝐤𝐮 𝐀𝐩𝐩 𝐍𝐚𝐦𝐞 🕊️𝐂𝐨𝐫𝐫𝐞𝐜𝐭...."
)
