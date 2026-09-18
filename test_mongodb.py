
import socket



_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only_getaddrinfo(*args, **kwargs):
    return [ai for ai in _orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = _ipv4_only_getaddrinfo

import pymongo
from dotenv import load_dotenv
import os
load_dotenv()
uri = os.getenv("MONGO_URL")

client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    print(client.admin.command("ping"))
    print("SUCCESS")
except Exception as e:
    print("FAILED:", e)