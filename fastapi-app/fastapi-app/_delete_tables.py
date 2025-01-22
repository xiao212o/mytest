from app import app_info
import models
import asyncio
from tortoise import Tortoise

async def run_app():
    await models.init(app_info.config().mysql.get_dsn())

    # 执行SQL语句
    sql = "SELECT CONCAT('ALTER TABLE ', table_name, ' DROP FOREIGN KEY ', constraint_name, ';') AS sql_statements FROM information_schema.key_column_usage WHERE constraint_schema = 'debugdb' AND referenced_table_name IS NOT NULL;"
    _,result = await Tortoise.get_connection('default').execute_query(sql)

    # 处理查询结果
    for row in result:
        # print(row)
        await Tortoise.get_connection('default').execute_query(row['sql_statements'])

    _,result = await Tortoise.get_connection('default').execute_query("show tables")
    # 处理查询结果
    for row in result:
        # print(row)
        await Tortoise.get_connection('default').execute_query("DROP TABLE {}".format(row['Tables_in_debugdb']))
    
def main():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_app())


if __name__ == '__main__':
    main()
