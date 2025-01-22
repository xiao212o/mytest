import datetime
import models
from tortoise.fields import (
    BooleanField,
    DatetimeField,
    DateField,
    TimeField,
    IntField,
    CharField,
    BigIntField,
    TextField,
    FloatField,
    JSONField,
    CharEnumField,
    IntEnumField,
    ForeignKeyRelation,
    ForeignKeyField,
    ReverseRelation,
    SET_NULL,
    ManyToManyField,
    ManyToManyRelation,
)
from .exceptions import ModelException

from tortoise.models import Model
from .fields import MyCharField, TimestampField

class BaseModel(Model):
    id = IntField(pk=True, description="ID")
    create_time = TimestampField(null=True, description="创建时间")
    
    class Meta:
        abstract = True

    def to_dict(self):
        result = {}
        for column, value in self:
            result[column] = value
        return result


class TagModel(BaseModel):
    name = MyCharField(100, null=False, description="名称")
    age = IntField(null=True, description="年龄")
    

    class Meta:
        table = "my_tag"


class BookModel(BaseModel):
    name = CharField(200, null=False, description="书名")
    author = CharField(100, null=True, description="作者")
    publication_time = DateField(null=True, description="出版时间")
    price = FloatField(null=True, description="价格")
    student = ForeignKeyField('models.StudentModel', related_name='books', null=False, description="关联的学生学号")

    class Meta:
        table = "my_book"

class StudentModel(BaseModel):
    name = CharField(200, null=False, description="学生姓名")
    gender = CharField(10, null=False, description="性别")
    age = IntField(pk=False,null=False, description="年龄")

    class Meta:
        table = "my_student"