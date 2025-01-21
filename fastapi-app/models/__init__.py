from tortoise import Tortoise
from tortoise.queryset import QuerySet
from .models import *


class Pagination(object):
    """
    分页对象
    """

    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items


async def paginate(self, page=1, per_page=10, callback=None, *, is_dict=True):
    """
    分页函数
    :param self:
    :param page:
    :param per_page:
    :param callback: if you want to do something for query_set,it will be useful.:
    :return:
    """
    if is_dict:
        items = await self.limit(per_page).offset((page - 1) * per_page).values()
    else:
        items = await self.limit(per_page).offset((page - 1) * per_page)

    if callback:
        """对查询集操作"""
        self = await callback(self)

    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = await self.count()

    return Pagination(self, page, per_page, total, items)


QuerySet.paginate = paginate


async def init(db_url):
    # globals()['SchoolModel'] = createClass(BaseModel, 'flow_school')

    # mysql_cfg = app_info.config().mysql
    await Tortoise.init(
        db_url=db_url,
        modules={
            "models": ["models.models", "models"]
        },
        use_tz=False,
        timezone="Asia/Shanghai"
    )
    await Tortoise.generate_schemas(safe=True)

    # from tortoise.connection import connections
    # await connections.all()[0].execute_query("alter table flow_school add yearxx int(11) default 0")

