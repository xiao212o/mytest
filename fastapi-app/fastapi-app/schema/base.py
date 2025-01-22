from pydantic.generics import GenericModel
from pydantic import BaseModel, PositiveInt, Field
from typing import Generic, TypeVar
from typing import List
from models.models import BookModel
from models.models import StudentModel

T = TypeVar('T')  # 泛型类型 T


class RestfulModel(GenericModel, Generic[T]):
    code: int = Field(0, title="code")
    msg: str = Field('', title="错误提示")
    data: T = None


class ModelId(BaseModel):
    id: PositiveInt


class Ids(BaseModel):
    ids: List[PositiveInt]

class Id(BaseModel):
    id: PositiveInt

class GetByIds(BaseModel):
    ids: List[PositiveInt]


class Search(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10000
    keyword: str = Field("", title="关键词")
    post_id: int = Field(None, title="岗位ID")


class AddResult(BaseModel):
    id: int = Field(0, title="自增ID")
    result: int = Field(0, title="成功标志")


class Result(BaseModel):
    result: int = Field(0, title="成功标志")

class SearchBook(BookModel):
    page : PositiveInt = 1
    page_size : PositiveInt = 10000
    keyword: str = Field("", title="关键词")
    post_id: int = Field(None, title="书籍ID")

class ResultBook(BookModel):
    result: int = Field(0, title="成功标志")

class SearchStudent(StudentModel):
    page : PositiveInt = 1
    page_size : PositiveInt = 10000
    keyword: str = Field("", title="关键词")
    post_id: int = Field(None, title="学生ID")

class ResultStudent(StudentModel):
    result: int = Field(0, title="成功标志")
