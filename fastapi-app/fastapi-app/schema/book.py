from pydantic import BaseModel,PositiveInt, Field, validator
from typing import List, Dict
from datetime import  date

class Add(BaseModel):
    name: str = Field("", title="书名")
    author: str = Field("", title="作者")
    publication_time: date = Field(title="出版时间")
    price: float = Field(0, title="价格")
    student_id: int = Field(1, title="学生ID")

class Edit(BaseModel):
    id: int = Field("",title="ID")
    name: str = Field("", title="书名")

class Remove(BaseModel):
    name: str = Field("",title="书名")
    author: str = Field("",title="作者")

class Search(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10000
    keyword: str = Field("", title="关键词")

class SearchForm(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10000
    keyword: str = Field("", title="关键词")

class Detail(BaseModel):
    id: int = Field(title="ID")
    name: str = Field("", title="书名")
    author: str = Field("", title="作者")
    create_time: str = Field(title="创建时间")
    publication_time: date = Field(title="出版时间")
    student: int = Field(title="学生ID")

class SearchList(BaseModel):
    result_list: List[Detail] = []
    total: int = 0