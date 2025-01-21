import functools
import traceback

from app import app_info, MyException
from fastapi import Header, Request
from tortoise.exceptions import IntegrityError


def decorator(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            result = await function(*args, **kwargs)
            if type(result) == dict:
                return {"code": 0, "msg": "", "data": result}
            else:
                return result
        except MyException as e:
            return {"code": e.code, "msg": e.message}
        except IntegrityError:
            if app_info.is_debug():
                app_info.logger().error(traceback.format_exc())
            return {"code": 1451, "msg": "关联数据错误"}
        except Exception as e:
            if app_info.is_debug():
                app_info.logger().error(traceback.format_exc())
            return {"code": 1, "msg": str(e)}

    return wrapper


class Context(object):
    def __init__(self, *, token=None, user=None, ip=None, request=None):
        self.token = token
        self.user = user
        self.ip = ip
        self.request = request

    def get_user(self):
        return self.user

    def get_user_id(self):
        return self.user.get("id")


async def verify_app(
    request: Request,
    x_forwarded_for_zl: str = Header(...),
    x_current_user_id: int = Header(...),
    x_current_username: str = Header(...),
):
    user = {
        "id": x_current_user_id,
        "name": x_current_username,
    }

    return Context(request=request, user=user, ip=x_forwarded_for_zl)


async def verify_app_inner(request: Request):
    return Context(request=request)
