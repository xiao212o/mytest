class ModelException(Exception):
    def __init__(self, code, message, data={}):
        self.code = code
        self.message = message
        self.data = data

    def output(self):
        return {
            "code": self.code,
            "msg": self.message,
            "data": {}
        }