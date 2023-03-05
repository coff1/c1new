from ..mydb import mydb
from .dingding import send_message_to_dingding
from .get_key_of_job import get_key_of_job

def write_done_to_db(id):
    #  返回任务在数据库内的数据量
    def count_of_job():
        key = get_key_of_job(id)
        sql_domain = "select count(*) from domain where " + \
            " or ".join(["domain = '{}'".format(i) for i in key])
        sql_subdomain = "select count(*) from subdomain where " + \
            " or ".join(["domain = '{}'".format(i) for i in key])
        sql_ip = "select count(*) from ip where " + \
            " or ".join(["ip = '{}'".format(i) for i in key])
        sql_url = "select count(*) from url where " + \
            " or ".join(["host like '%{}%'".format(i) for i in key])
        sql_sensitiveinfo = "select count(*) from sensitiveinfo where "+" or ".join([
            "url like '%{}%'".format(i) for i in key])
        count = 0
        for i in [sql_url, sql_domain, sql_ip, sql_sensitiveinfo, sql_subdomain]:
            # print(i)
            n = mydb().query_sqlite(i)["result"][0][0]
            count += n
            # print(i, "\n", n)
        return count

    #  返回任务在数据库内新的数据量
    def count_of_job_new():
        key = get_key_of_job(id)
        sql_domain = "select count(*) from domain where ("+" or ".join(
            ["domain = '{}'".format(i) for i in key])+") and is_new = 1"
        sql_subdomain = "select count(*) from subdomain where ("+" or ".join(
            ["domain = '{}'".format(i) for i in key])+") and is_new = 1"
        sql_ip = "select count(*) from ip where ("+" or ".join(
            ["ip = '{}'".format(i) for i in key])+") and is_new = 1"
        sql_url = "select count(*) from url where ("+" or ".join(
            ["host like '%{}%'".format(i) for i in key])+") and is_new = 1"
        sql_sensitiveinfo = "select count(*) from sensitiveinfo where ("+" or ".join(
            ["url like '%{}%'".format(i) for i in key])+") and is_new = 1"
        count = 0
        for i in [sql_url, sql_domain, sql_ip, sql_sensitiveinfo, sql_subdomain]:
            n = mydb().query_sqlite(i)["result"][0][0]
            count += n
            # print(i, "\n", n)
        return count

    x = mydb()
    job_num=count_of_job()
    job_new_num=count_of_job_new()
    send_message_to_dingding("任务完成！\nid:{}\n资产总计:{}\n新资产:{}".format(id,job_num,job_new_num))
    x.execute_sqlite("update task set status = '已完成' , count = {} ,count_new = {} where id = {}".format(
        job_num, job_new_num, id))