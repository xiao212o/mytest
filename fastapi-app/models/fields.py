from tortoise import fields


class TimestampField(fields.DatetimeField):
    class _db_mysql:
        SQL_TYPE = "TIMESTAMP NULL DEFAULT NULL"

    def to_python_value(self, value):
        if value is None:
            return None
        return str(value).split(".")[0]


class MyCharField(fields.CharField):
    def to_python_value(self, value):
        if value is None:
            return ''

        return value


class TextField(fields.TextField):
    def to_python_value(self, value):
        if value is None:
            return ''

        return value
