from fastapi import APIRouter, Depends
from app import app_info
import datetime
import models
from router.base import decorator, verify_app
from schema import student, base
from tortoise.transactions import atomic

tags = ["tag"]

router = APIRouter()

@router.post("/student/add", tags=tags, response_model=base.RestfulModel[base.AddResult], name="添加学生")
@decorator
@atomic()
async def student_add(param: student.Add):
    record = models.StudentModel(
        **param.dict(),
        create_time=datetime.datetime.now(),
        update_time=datetime.datetime.now(),
    )
    await record.save()

    return {
        "result": 1,
        "id": record.id
    }



@router.post("/student/edit", tags=tags, response_model=base.RestfulModel[base.Result], name="修改学生信息")
@decorator
@atomic()
async def student_edit(param: student.Edit):
    record = await models.StudentModel.filter(id=param.id).first()
    if record:
        record.name = param.name
        record.age = param.age
        record.gender = param.gender
        await record.save()
    else:
        app_info.raise_except(1, "记录不存在")

    return {
        "result":1,
    }


@router.post("/student/remove", tags=tags, response_model=base.RestfulModel[base.Result], name="删除学生信息")
@decorator
@atomic()
async def student_remove(param: base.Id):
    row = await models.StudentModel.filter(pk=param.id).first()
    if not row:
        app_info.raise_except(1, "记录不存在")

    await row.delete()

    return {"result": 1}


@router.post("/student/search", tags=tags, response_model=base.RestfulModel[student.SearchList], name="搜索学生信息")
@decorator
async def student_search(param: student.SearchForm):
    if param.keyword and len(param.keyword) > 0:
        query = models.StudentModel.all().filter(name__contains=param.keyword)
    else:
        query = models.StudentModel.all()

    query = query.order_by("id")

    pagination = await query.paginate(param.page, param.page_size, is_dict=False)

    result_list = []
    for item in pagination.items:
        info = item.to_dict()
        result_list.append(info)

    return {"result_list": result_list, "total": pagination.total}


