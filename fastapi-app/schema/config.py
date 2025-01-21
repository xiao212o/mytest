from pydantic import BaseModel
from typing import List
from loguru import logger

class Logger(BaseModel):
    level: str = 'INFO'
    retention: str = '7 days'
    compression: str = 'zip'
    rotation: str = '00:00'
    log_path: str = "/var/log"

    def initial(self, filename=None):
        if filename!=None:
            filename = '{}/{}'.format(self.log_path, filename)
            logger.add(filename, rotation=self.rotation, retention=self.retention, compression=self.compression, level=self.level)

        return logger

class ConfigModule(BaseModel):
    debug: bool = False
    workers: int = 10

class Mysql(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

    def get_dsn(self):
        return "mysql://{}:{}@{}:{}/{}".format(
            self.user, 
            self.password, 
            self.host, 
            self.port, 
            self.name,
        )

class Config(BaseModel):
    module: ConfigModule
    mysql: Mysql
    logger: Logger
