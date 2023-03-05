from ..mydb import mydb
from ..mylist import mylist
from..myurl import myurl
# def get_key_of_job(id) -> list:
#     def get_key_of_company_s(task_company):
#         sql = """select domain from domain where"""
#         sql += " or ".join([" company = '{}' ".format(i)
#                             for i in task_company])
#         print(sql)
#         domain_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]

#         sql = """
#             SELECT distinct subdomain.ip
#             FROM subdomain
#             JOIN ip
#             ON subdomain.ip = ip.ip
#             WHERE 
#         """
#         sql = sql + \
#             " or ".join(["subdomain.domain= '{}'".format(i)
#                         for i in mylist(task_company,domain_key).my_list])
#         ip_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]

#         return mylist(ip_key, domain_key).my_list

#     def get_key_of_domain_s(task_domain):
#         sql = """
#             SELECT distinct ip from subdomain where 
#         """
#         sql = sql + " or ".join(["domain = '{}'".format(i)
#                                 for i in task_domain])
#         ip_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]
#         domain_key = task_domain
#         return mylist(ip_key, domain_key).my_list

#     def get_key_of_url_s(task_url):
#         return [myurl(i).get_domain_root() for i in task_url]

#     def get_key_of_ip_s(task_ip):
#         return task_ip[:]

#     sql = """
#         select target from task where id = {}
#     """.format(id)
#     task = (mydb().query_sqlite(sql)["result"][0][0]).split("\t")
#     task = mylist(task)
#     task_key = mylist()
#     task_company = task.extract_company_from_list()
#     task_ip = task.extract_ip_from_list()
#     task_url = task.extract_url_from_list()
#     task_domain = task.extract_domain_from_list()
#     if len(task_company) > 0:
#         task_key.concat_lists(get_key_of_company_s(task_company))

#     if len(task_domain) > 0:
#         task_key.concat_lists(get_key_of_domain_s(task_domain))

#     if len(task_url) > 0:
#         task_key.concat_lists(get_key_of_url_s(task_url))

#     if len(task_ip) > 0:
#         task_key.concat_lists(get_key_of_ip_s(task_ip))

#     print(task_key.my_list)
#     return task_key.my_list

def get_key_of_job(id) -> list:
    def get_key_of_company_s(task_company):
        sql = """select domain from domain where company in ("""
        sql += ",".join(["'{}'".format(i) for i in task_company])+")"
        print(sql)

        domain_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]

        sql = """
            SELECT distinct subdomain.ip
            FROM subdomain
            JOIN ip
            ON subdomain.ip = ip.ip
            WHERE subdomain.domain in (
        """
        sql = sql + \
            ",".join(["'{}'".format(i) for i in mylist(task_company,domain_key).my_list])+")"
        
        ip_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]

        sql = """
            SELECT distinct subdomain
            FROM subdomain
            WHERE domain in (
        """
        sql = sql + \
            ",".join(["'{}'".format(i) for i in mylist(task_company,domain_key,ip_key).my_list])+")"
        subdomain_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]


        sql = """
            SELECT distinct url
            FROM url
            WHERE host in (
        """
        sql = sql + \
            ",".join(["'{}'".format(i) for i in mylist(task_company,domain_key,ip_key,subdomain_key).my_list])+")"
        url_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]


        return mylist(ip_key, domain_key , subdomain_key ,url_key).my_list

    def get_key_of_domain_s(task_domain):
        sql = """
            SELECT distinct ip from subdomain where 
        """
        sql = sql + " or ".join(["domain = '{}'".format(i)
                                for i in task_domain])
        ip_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]

        domain_key = task_domain

        sql = """
            SELECT distinct subdomain
            FROM subdomain
            WHERE domain in (
        """
        sql = sql + \
            ",".join(["'{}'".format(i) for i in mylist(domain_key,ip_key).my_list])+")"
        subdomain_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]


        sql = """
            SELECT distinct url
            FROM url
            WHERE host in (
        """
        sql = sql + \
            ",".join(["'{}'".format(i) for i in mylist(domain_key,ip_key,subdomain_key).my_list])+")"
        url_key = [i[0] for i in mydb().query_sqlite(sql)["result"]]


        return mylist(ip_key, domain_key,subdomain_key,url_key).my_list


    def get_key_of_url_s(task_url):
        domain_root_key =  [myurl(i).get_domain_root for i in task_url]
        domain_key = [myurl(i).get_domain for i in task_url]
        return get_key_of_domain_s(mylist(domain_root_key,domain_key).my_list)

    def get_key_of_ip_s(task_ip):
        return task_ip[:]

    sql = """
        select target from task where id = {}
    """.format(id)
    task = (mydb().query_sqlite(sql)["result"][0][0]).split("\t")
    task = mylist(task)
    task_key = mylist()
    task_company = task.extract_company_from_list()
    task_ip = task.extract_ip_from_list()
    task_url = task.extract_url_from_list()
    task_domain = task.extract_domain_from_list()
    if len(task_company) > 0:
        task_key.concat_lists(get_key_of_company_s(task_company))

    if len(task_domain) > 0:
        task_key.concat_lists(get_key_of_domain_s(task_domain))

    if len(task_url) > 0:
        task_key.concat_lists(get_key_of_url_s(task_url))

    if len(task_ip) > 0:
        task_key.concat_lists(get_key_of_ip_s(task_ip))

    print(task_key.my_list)
    return task_key.my_list