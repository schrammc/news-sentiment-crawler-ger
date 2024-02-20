from dotenv import load_dotenv
import os
import logging


class Config:
    """A configuration for the app, implemented as a singleton"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            logging.debug("Initializing config")
            load_dotenv()

            cls.__instance = super().__new__(cls)
            mongo_host = os.getenv("MONGO_HOST")
            mongo_user = os.getenv("MONGO_USER")
            mongo_password = os.getenv("MONGO_PASSWORD")
            cls.__instance.mongo_host = mongo_host
            cls.__instance.mongo_user = mongo_user
            cls.__instance.mongo_password = mongo_password

            logging.debug(f"Initialized config. mongo_host is {mongo_host}")
        return cls.__instance
