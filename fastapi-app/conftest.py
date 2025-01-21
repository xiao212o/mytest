import traceback

import pytest
from httpx import AsyncClient

import models

class TestClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def post(
        self, url, data=None, *, user_id="1", username="admin", ip="192.168.1.1"
    ):
        headers = {
            "x-forwarded-for-zl": ip,
            "x-current-user-id": str(user_id),
            "x-current-username": username,
        }

        response = await self.client.post(url, json=data, headers=headers)

        if response.status_code != 200:
            print(f"Request URL: {url}")  # 打印请求 URL
            print(f"Request Data: {data}")  # 打印请求数据
            print(f"Response Status Code: {response.status_code}")  # 打印响应状态码
            print(f"Response Content: {response.content}")  # 打印响应内容
            return 1, response.content, {}

        try:
            res = response.json()
            return res["code"], res["msg"], res.get("data", None)
        except Exception:
            traceback.print_exc()

    async def get(self, url, *, user_id="1", username="admin", ip="192.168.1.1"):
        headers = {
            "x-forwarded-for-zl": ip,
            "x-current-user-id": str(user_id),
            "x-current-username": username,
        }

        response = await self.client.get(url, headers=headers)

        if response.status_code != 200:
            return 1, response.content, {}

        try:
            return response.json()
        except Exception:
            traceback.print_exc()


@pytest.fixture(scope="session")
def anyio_backend():
    # print("Client is ready", '===')
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    from index import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        # print("Client is ready")
        yield TestClient(client)


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    from app import app_info

    db_url = app_info.config().mysql.get_dsn()

    await models.init(db_url)

    # yield
    # await Tortoise._drop_databases()
