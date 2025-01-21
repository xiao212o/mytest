from lib.singleton import singleton
from schema.config import Config
import json
import logging

class MyException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def output(self):
        return {"code": self.code, "msg": self.message, "data": {}}

class App:
    def __init__(self):
        self.MyException = MyException

    @singleton
    def config(self) -> Config:
        with open("config/config.json") as f:
            txt = f.read()
            config = json.loads(txt)

            return Config(**config)

    @singleton
    def logger(self):
        return self.config().logger.initial()

    def raise_except(self, code, message):
        raise MyException(code, message)

    @staticmethod
    def is_debug():
        return app_info.config().module.debug




app_info = App()
