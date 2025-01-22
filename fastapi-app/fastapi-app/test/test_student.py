import datetime
import test
import pytest
import models
from app import app_info
#name="jammiy", age=14, gender="男",

@pytest.fixture(scope='function', autouse=True)
async def func_scope():
    await test.clear_db()

@pytest.mark.anyio
async def test_add_4(client):
    data = {
        "name": "张三",
        "gender": "男",
        "age": 14,
    }

    code, msg, result = await client.post("/student/add", data=data)

    assert code == 0, msg
    assert result["id"] > 0
    assert result["result"] == 1
    # print(result)

    record = await models.StudentModel.filter(pk=result["id"]).first()
    assert record.name == "张三"
    assert record.age == 14
    assert record.create_time is not None
    assert record.gender == "男"
    # print(result)

@pytest.mark.anyio
async def test_edit_4(client):
    await test.get_student(id=1)
    data = {
        "id": 1,
        "name": "李四",
        "gender": "女",
        "age": 15,
    }

    code, msg, result = await client.post("/student/edit", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.StudentModel.filter(pk=1).first()
    assert record.name == "李四"
    assert record.age == 15
    assert record.gender == "女"
    assert record.create_time is not None


@pytest.mark.anyio
async def test_remove_4(client):
    await test.get_student(id=1)
    data = {
        "id": 1,
        "name": "wangwu",
        "age": 16,
    }

    code, msg, result = await client.post("/student/remove", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.StudentModel.filter(pk=1).first()
    assert record is None


@pytest.mark.anyio
async def test_search_5(client):
    await test.get_student(id=1, name="jammiy", age=14, gender="男", create_time='2024-03-01 00:00:00')
    await test.get_student(id=2, name="cody", age=14, gender="男", create_time='2024-03-01 00:00:00')
    await test.get_student(id=3, name="bron", age=14, gender="男", create_time='2024-03-01 00:00:00')


    code, msg, ret = await client.post("/student/search", data={
        "keyword": "",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 3

    record = ret["result_list"][0]
    assert record["id"] == 1
    assert record["name"] == "jammiy"
    assert record['create_time'] is not None


@pytest.mark.anyio
async def test_search_6(client):
    await test.get_student(id=1, name="alpha", age=14, gender="男", create_time='2024-03-01 00:00:00')
    await test.get_student(id=2, name="sigmod", age=16, gender="女", create_time='2024-03-03 00:00:00')
    await test.get_student(id=3, name="build", age=18, gender="男", create_time='2024-03-06 00:00:00')


    code, msg, ret = await client.post("/student/search", data={
        "keyword": "alpha",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 1

    record = ret["result_list"][0]
    assert record["id"] == 1
    assert record["name"] == "alpha"
    assert record["gender"] == "男"
    assert record["age"] == 14
    assert record['create_time'] is not None


