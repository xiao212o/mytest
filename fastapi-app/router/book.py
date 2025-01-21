from fastapi import APIRouter, Depends
from app import app_info
import datetime
import models
from router.base import decorator, verify_app
from schema import book, base
from tortoise.transactions import atomic
from models import BookModel, StudentModel

tags = ["tag"]

router = APIRouter()

@router.post("/book/add", tags=tags, response_model=base.RestfulModel[base.AddResult], name="添加书籍")
@decorator
@atomic()
async def book_add(param: book.Add):
    record = models.BookModel(
        **param.dict(),
        create_time=datetime.datetime.now(),
        update_time=datetime.datetime.now(),
    )
    await record.save()

    return {
        "result": 1,
        "id": record.id
    }



@router.post("/book/edit", tags=tags, response_model=base.RestfulModel[base.Result], name="修改标签书籍")
@decorator
@atomic()
async def book_edit(param: book.Edit):
    record = await models.BookModel.filter(id=param.id).first()
    if record:
        record.name = param.name
        await record.save()
    else:
        app_info.raise_except(1, "记录不存在")

    return {
        "result": 1,"name": "python爬虫教学"
    }


@router.post("/book/remove", tags=tags, response_model=base.RestfulModel[base.Result], name="删除标签书籍")
@decorator
@atomic()
async def book_remove(param: base.Id):
    row = await models.BookModel.filter(pk=param.id).first()
    if not row:
        app_info.raise_except(1, "记录不存在")

    await row.delete()

    return {"result": 1}


@router.post("/book/search", tags=tags, response_model=base.RestfulModel[book.SearchList], name="搜索标签书籍")
@decorator
async def book_search(param: book.SearchForm):
    if param.keyword and len(param.keyword) > 0:
        query = models.BookModel.all().filter(name__contains=param.keyword)
    else:
        query = models.BookModel.all()

    query = query.order_by("id")

    pagination = await query.paginate(param.page, param.page_size, is_dict=False)

    result_list = []
    for item in pagination.items:
        info = item.to_dict()
        result_list.append(info)

    return {"result_list": result_list, "total": pagination.total}

from fastapi import APIRouter
from models import BookModel, StudentModel

router = APIRouter()

@router.get("/book/{book_id}/student")
async def get_book_student(book_id: int):
    # 根据 book_id 查询 BookModel 记录
    book = BookModel.get_or_none(BookModel.id == book_id)
    if book:
        # 根据 BookModel 中的 student_id 查询对应的 StudentModel 记录
        student = StudentModel.get_or_none(StudentModel.id == book.student_id)
        if student:
            student_info = {
                "id": student.id,
                "name": student.name,
                "gender": student.gender,
                "age": student.age
            }
            return {"student_info": student_info}
        else:
            return {"message": "关联的学生信息不存在"}
    else:
        return {"message": "书籍信息不存在"}
