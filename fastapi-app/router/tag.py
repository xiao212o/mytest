from fastapi import APIRouter, Depends
import datetime
from app import app_info
import models
from router.base import decorator, verify_app
from schema import tag, base
from tortoise.transactions import atomic

tags = ["tag"]

router = APIRouter()

@router.post("/tag/add", tags=tags, response_model=base.RestfulModel[base.AddResult], name="添加标签")
@decorator
@atomic()
async def tag_add(param: tag.Add):
    record = models.TagModel(
        **param.dict(),
        create_time=datetime.datetime.now(),
        update_time=datetime.datetime.now(),
    )
    await record.save()

    return {
        "result": 1,
        "id": record.id
    }


@router.post("/tag/edit", tags=tags, response_model=base.RestfulModel[base.Result], name="修改标签")
@decorator
@atomic()
async def tag_edit(param: tag.Edit):
    record = await models.TagModel.filter(id=param.id).first()
    if record:
        record.name = param.name
        await record.save()
    else:
        app_info.raise_except(1, "记录不存在")

    return {
        "result": 1,
    }

@router.post("/tag/remove", tags=tags, response_model=base.RestfulModel[base.Result], name="删除标签")
@decorator
@atomic()
async def tag_remove(param: base.Id):
    row = await models.TagModel.filter(pk=param.id).first()
    if not row:
        app_info.raise_except(1, "记录不存在")

    await row.delete()

    return {"result": 1}



@router.post("/tag/search", tags=tags, response_model=base.RestfulModel[tag.SearchList], name="搜索标签")
@decorator
async def search(param: tag.SearchForm):
    if param.keyword and len(param.keyword)>0:
        query = models.TagModel.all().filter(name__contains=param.keyword)
    else:
        query = models.TagModel.all()

    query = query.order_by("id")

    pagination = await query.paginate(param.page, param.page_size, is_dict=False)

    result_list = []
    for item in pagination.items:
        info = item.to_dict()
        result_list.append(info)

    return {"result_list": result_list, "total": pagination.total}
