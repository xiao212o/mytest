import datetime
import test
import pytest
import models
from app import app_info


@pytest.fixture(scope='function', autouse=True)
async def func_scope():
    await test.clear_db()


@pytest.mark.anyio
async def test_add_1(client):
    data = {
        "name": "交朋友",
    }

    code, msg, result = await client.post("/tag/add", data=data)

    assert code == 0, msg
    assert result["id"] > 0
    assert result["result"] == 1

    # print(result)

    record = await models.TagModel.filter(pk=result["id"]).first()
    assert record.name == "交朋友"
    assert record.create_time is not None


@pytest.mark.anyio
async def test_edit_1(client):
    await test.get_tag(id=1)
    data = {
        "id": 1,
        "name": "交朋友",
    }

    code, msg, result = await client.post("/tag/edit", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.TagModel.filter(pk=1).first()
    assert record.name == "交朋友"
    assert record.create_time is not None


@pytest.mark.anyio
async def test_remove_1(client):
    await test.get_tag(id=1)
    data = {
        "id": 1,
    }

    code, msg, result = await client.post("/tag/remove", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.TagModel.filter(pk=1).first()
    assert record is None


@pytest.mark.anyio
async def test_search_1(client):
    await test.get_tag(id=1, name="交朋友", age=14, create_time='2024-03-01 00:00:00')
    await test.get_tag(id=2, name="加油", age=14, create_time='2024-03-01 00:00:00')
    await test.get_tag(id=3, name="主播优秀", age=14, create_time='2024-03-01 00:00:00')


    code, msg, ret = await client.post("/tag/search", data={
        "keyword": "",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 3

    record = ret["result_list"][0]
    assert record["id"] == 1
    assert record["name"] == "交朋友"
    assert record['create_time'] is not None


@pytest.mark.anyio
async def test_search_2(client):
    await test.get_tag(id=1, name="交朋友", age=14, create_time='2024-03-01 00:00:00')
    await test.get_tag(id=2, name="加油", age=14, create_time='2024-03-01 00:00:00')
    await test.get_tag(id=3, name="主播优秀", create_time='2024-03-01 00:00:00')


    code, msg, ret = await client.post("/tag/search", data={
        "keyword": "朋友",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 1

    record = ret["result_list"][0]
    assert record["id"] == 1
    assert record["name"] == "交朋友"
    assert record['create_time'] is not None



