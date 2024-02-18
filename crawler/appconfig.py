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
            cls.__instance.mongo_host = os.getenv("MONGO_HOST")
        return cls.__instance
