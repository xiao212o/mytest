import models

async def clear_db():
    await models.TagModel.all().delete()
    await models.BookModel.all().delete()
    await models.StudentModel.all().delete()


async def get_tag(**kwargs):
    data = {
        "name": "demo",
        "create_time": "2021-01-01 00:00:00",
    }

    for k, v in kwargs.items():
        data[k] = v

    record = models.TagModel(**data)
    await record.save()
    return record

async def get_book(**kwargs):
    data = {
        "name": "demo",
        "create_time": "2025-01-01 00:00:00",
    }
    for k, v in kwargs.items():
        data[k] = v

    record = models.BookModel(**data)
    await record.save()
    return record

async def get_student(**kwargs):
    data = {
        "name": "demo",
        "age": 1,
        "gender": "male",
        "create_time": "2025-01-16 00:00:00",
    }
    for k, v in kwargs.items():
        data[k] = v

    record = models.StudentModel(**data)
    await record.save()
    return record