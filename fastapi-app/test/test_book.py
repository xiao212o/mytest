import datetime
import test
import pytest
import models
from app import app_info


@pytest.fixture(scope='function', autouse=True)
async def func_scope():
    await test.clear_db()

@pytest.mark.anyio
async def test_add_3(client):
    data = {
        "name": "昆虫百科",
        "author": "达尔文",
        "publication_time": "2025-01-15"
    }

    code, msg, result = await client.post("/book/add", data=data)

    assert code == 0, msg
    assert result["id"] > 0
    assert result["result"] == 1

    # print(result)

    record = await models.BookModel.filter(pk=result["id"]).first()
    assert record.name == "昆虫百科"
    assert record.author == "达尔文"
    assert record.publication_time.strftime('%Y-%m-%d') == "2025-01-15"
    assert record.price is not None

@pytest.mark.anyio
async def test_edit_2(client):
    await test.get_book(id=1)
    data = {
        "id": 1,
        "name": "python爬虫教学",
    }

    code, msg, result = await client.post("/book/edit", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.BookModel.filter(pk=1).first()
    assert record.name == "python爬虫教学"
    assert record.create_time is not None

@pytest.mark.anyio
async def test_remove_2(client):
    await test.get_book(id=1)
    data = {
        "id": 1,
    }

    code, msg, result = await client.post("/book/remove", data=data)

    assert code == 0, msg
    assert result["result"] == 1

    # print(result)

    record = await models.BookModel.filter(pk=1).first()
    assert record is None

@pytest.mark.anyio
async def test_search_3(client):
    await test.get_book(id=1, name="交朋友", author="abc", publication_time='2008-01-01', create_time='2024-03-01 00:00:00')
    await test.get_book(id=2, name="加油",  author="abc", publication_time='2008-01-01', create_time='2024-03-01 00:00:00')
    await test.get_book(id=3, name="主播优秀",  author="abc", publication_time='2008-01-01',create_time='2024-03-01 00:00:00')


    code, msg, ret = await client.post("/book/search", data={
        "keyword": "",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 3

    record = ret["result_list"][0]
    assert record["id"] == 1
    assert record["name"] == "交朋友"
    assert record["author"] == "abc"
    assert record["publication_time"] == "2008-01-01"
    assert record['create_time'] is not None

@pytest.mark.anyio
async def test_search_4(client):
    await test.get_book(id=1, name="javaspring", author= "aaa", publication_time='2008-01-01', create_time='2024-03-02 00:00:00')
    await test.get_book(id=2, name="mySQLgo", author= "bbb", publication_time='2008-02-01', create_time='2024-03-01 00:00:00')
    await test.get_book(id=3, name="python", author= "ccc", publication_time='2008-03-01', create_time='2024-04-01 00:00:00')


    code, msg, ret = await client.post("/book/search", data={
        "keyword": "python",
        "page": 1,
        "page_size": 5,
    })
    assert code == 0, msg
    assert len(ret["result_list"]) == 1

    record = ret["result_list"][0]
    assert record["id"] == 3
    assert record["name"] == "python"
    assert record["author"] == "ccc"
    assert record["publication_time"] == "2008-03-01"
    assert record['create_time'] is not None