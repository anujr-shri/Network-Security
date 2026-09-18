import socket

_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only_getaddrinfo(*args, **kwargs):
    return [ai for ai in _orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = _ipv4_only_getaddrinfo

from pymongo import MongoClient
from src.exceptions.exception import NetworkSecurityException
from src.logging.logging import get_logger
from dotenv import load_dotenv
import pandas as pd
import json
import os
import sys
import certifi

ca = certifi.where()

load_dotenv()
MONGO_URL = os.getenv("MONGO_DB_URLL")
print(MONGO_URL)
FILE_PATH = "Network_Data\\phisingData.csv"
logger = get_logger(__name__)

class NetworkETL:

    def load_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            data_json = list(json.loads(data.T.to_json()).values())
            return data_json

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def load_data_into_mongodb(self, database, collection, records):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = MongoClient(MONGO_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            logger.error("Cannot Upload The Data Into Mongo Db")
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    newtwork_etl = NetworkETL()

    data = newtwork_etl.load_to_json(FILE_PATH)
    newtwork_etl.load_data_into_mongodb("network", "phisingData", data)