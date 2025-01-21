from pydantic import constr
from datetime import datetime

Str_10 = constr(strip_whitespace=True, max_length=10)
Str_10_No_Empty = constr(strip_whitespace=True, min_length=1, max_length=10)


class DateTime(str):
    # default = time.strftime("%Y-%m-%d", time.localtime())
    default = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "" or v is None or v == "null":
            return cls.default

        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except(TypeError, ValueError):
            raise ValueError("参数不是时间类型")


class Date(str):
    # default = time.strftime("%Y-%m-%d", time.localtime())
    default = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "" or v is None or v == "null":
            return cls.default

        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except(TypeError, ValueError):
            raise ValueError("参数不是日期类型")  
class Time(str):
    # default = time.strftime("%Y-%m-%d", time.localtime())
    default = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == "" or v is None or v == "null":
            return cls.default

        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except(TypeError, ValueError):
            raise ValueError("参数不是时间类型")
