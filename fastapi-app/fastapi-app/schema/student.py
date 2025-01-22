from pydantic import BaseModel,PositiveInt, Field, validator
from typing import List, Dict, Optional
from datetime import  date

class Add(BaseModel):
    name: str = Field("", title="姓名")
    gender: str = Field("", title="性别")
    age: int = Field(0, title="年龄")
    student_id: int = Field("", title="学号")


class Edit(BaseModel):
    id: int = Field(title="ID")
    name: str = Field("", title="姓名")
    gender: str = Field("", title="性别")
    age: int = Field(0, title="年龄")

class Remove(BaseModel):
    name: str = Field("", title="姓名")
    gender: str = Field("", title="性别")
    age: int = Field(0, title="年龄")

class Search(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10000
    keyword: str = Field("", title="关键词")

class SearchForm(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10000
    keyword: str = Field("", title="关键词")

class Detail(BaseModel):
    id: int = Field(title="学号")
    name: str = Field("", title="姓名")
    gender: str = Field("", title="性别")
    age: int = Field(title="年龄")
    create_time: str = Field(title="创建时间")
    studentid_id: int = Field("", title="学号")

class SearchList(BaseModel):
    result_list: List[Detail] = []
    total: int = 0
