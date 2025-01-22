import uvicorn
from fastapi import FastAPI
import models
from app import app_info, MyException
from router.autoload import routers
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

async def request_validation_exception_handler_422(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    捕捉422报错并进行自定义处理
    :param request:
    :param exc:
    :return:
    """
    array = []
    for item in exc.errors():
        msg = item['msg']
        field = item['loc'][-1]

        if item['type']=="value_error.missing" and msg=='field required':
            msg = '字段不能为空'
        elif item['type']=='value_error.jsondecode':
            msg = "参数格式错误"
            field = ""

        array.append({
            'field': field,
            'msg': msg

        })

    status_code = 200
    return JSONResponse(
        status_code=status_code,
        content={
            "code": 422,
            "msg": "",
            "data": {
                "detail": array,
                "debug": exc.errors()
            }
        },
    )

async def request_myexception_handler(request: Request, exc: MyException) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=exc.output(),
    )


if app_info.is_debug():
    prefix = ""
    app = FastAPI()
else:
    prefix = ""
    app = FastAPI(docs_url=None, redoc_url=None)

@app.on_event("startup")
async def init_db():
    db_url = app_info.config().mysql.get_dsn()
    await models.init(db_url)


app.add_exception_handler(RequestValidationError, request_validation_exception_handler_422)
app.add_exception_handler(MyException, request_myexception_handler)

for row in routers:
    app.include_router(row)


def main():
    workers = app_info.config().module.workers
    app_info.logger().info("服务启动正在启动 workers={}".format(workers))
    uvicorn.run("index:app", host="0.0.0.0", port=8000, workers=workers)


if __name__ == "__main__":
    main()
