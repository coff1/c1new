from ..mydb import mydb
from .get_key_of_job import get_key_of_job
def get_task_data_by_id(id)->dict:
    # key = get_key_of_job(id)
    # sql_domain = "select * from domain  where " + \
    #     " or ".join(["domain = '{}'".format(i) for i in key])+"order by company"
    # sql_subdomain = "select * from subdomain where " + \
    #     " or ".join(["domain = '{}'".format(i) for i in key])+"order by domain "
    # sql_ip = "select * from ip  where " + \
    #     " or ".join(["ip like '%{}%'".format(i) for i in key])+"order by ip"
    # print(sql_ip)
    # sql_url = "select * from url where " + \
    #     " or ".join(["host like '%{}%'".format(i) for i in key])+"order by host,length(url) "
    # sql_sensitiveinfo = "select * from sensitiveinfo where "+" or ".join([
    #     "url like '%{}%'".format(i) for i in key])+"order by quantity DESC "
    # sql_website = "SELECT * from  url  where "+\
    #     " or ".join(["host like '%{}%'".format(i) for i in key])+" group by website order by status_code,host ASC,length(title),content_length desc "
    
    key = get_key_of_job(id)
    sql_domain = "select * from domain  where domain in (" + \
        ",".join(["'"+i+"'" for i in key])+") order by company"
    
    sql_subdomain = "select * from subdomain where domain in (" + \
        ",".join(["'"+i+"'" for i in key])+") order by domain "
    
    sql_ip = "select * from ip  where ip in (" + \
        ",".join(["'"+i+"'" for i in key])+") order by ip"
    
    # print(sql_ip)
    sql_url = "select * from url where host in (" + \
        ",".join(["'"+i+"'" for i in key])+") order by host,length(url) "
    
    sql_sensitiveinfo = "select * from sensitiveinfo where url in ("+ \
        ",".join(["'"+i+"'" for i in key])+") order by quantity DESC "
    
    sql_website = "SELECT * from  url  where host in ("+\
        ",".join(["'"+i+"'" for i in key])+")  group by website order by status_code,host ASC,length(title),content_length desc "


    page_name=[
        'url',
        'domain',
        'ip',
        'sensitiveinfo',
        'subdomain',
        'website'
    ]
    # num=0
    result = list()
    field_names = list()
    # 这里不能用mylist类，避免自动去重
    for i in [sql_url, sql_domain, sql_ip, sql_sensitiveinfo, sql_subdomain,sql_website]:
        # print(i)
        temp_data=mydb().query_sqlite(i)
        result.append(temp_data["result"])
        field_names.append(temp_data["field_names"])

    return {'page_name':page_name,'field_names':field_names,'result':result}