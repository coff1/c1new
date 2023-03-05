from .mydb import mydb
from .myhost import myhost
from .myinfoget import myinfoget
from .mylist import mylist
from .myrequests import myrequests
from .myurl import myurl
from concurrent.futures import ThreadPoolExecutor, as_completed
from source.config import config
from source.myclass.mylog import mylog
# 功能集成
# 如获取xxx的信息

class myassembly:
    def __init__(self,do_crawler=False) -> None:
        self.do_crawler=do_crawler
        self.type=""
        self.target=[]
        self.describe=""
        self.key=[]

    # 获取某个链接的信息
    def base_get_info_of_url(self,url):

        x=myinfoget(url)
        db=mydb()
        db.insert_or_update_table("url",{
            "website":x.get_base_path(),
            "host":x.get_hostname(),
            "url":url,
            "url_type":x.type,
            "title":x.get_title(),
            "status_code":x.status_code,
            "content_length":x.length,
            # "response_text":x.text
            "response_text":""
        })
        sensitive_info=x.get_sensitive_information()
        if sensitive_info["quantity"]>0:
            db.insert_or_update_table("sensitiveinfo",{
                "url":url,
                "phone":"|".join(sensitive_info["phone"]),
                "email":"|".join(sensitive_info["email"]),
                "idcard":"|".join(sensitive_info["idcard"]),
                "credentials":"|".join(sensitive_info["credentials"]),
                "quantity":sensitive_info["quantity"]
            })
            # print("success")
        return {"link_by_domain":x.get_link_by_domain_root(),"link_by_host":x.get_link_by_host()}
    # 获取多个链接的信息
    def base_get_info_of_url_s(self,url_s):
        for url in url_s:
            self.base_get_info_of_url(url)


    # 启用爬虫，对单个url进行爬取 ，这个没用
    def crawler_info_from_url(self,url):
        urls=[url]
        self.crawler_info_from_url_s(urls)

    # 启用爬虫，对多个url进行爬取 ， 这个有用 
    def crawler_info_from_url_s(self,urls,target = 'host'):

        url_all=mylist(urls)
        num=config.crawler_depth
        for i in range(0,num):
            if len(url_all.get_my_list_new())==0:
                break
            url_temp=mylist()
            # 没有爬取过的链接
            url_new=url_all.get_my_list_new()

            def crawler(i):
                url_all.out_one_from_list()
                try:
                    # 提取网页链接
                    if target == 'host':
                        url_temp.concat_lists(self.base_get_info_of_url(i)["link_by_host"])
                    if target == 'domain':
                        url_temp.concat_lists(self.base_get_info_of_url(i)["link_by_domain"])
                except BaseException:
                    message = "{} 访问失败".format(i)
                    mylog().info(message)
                    pass

            with ThreadPoolExecutor(max_workers=10) as t:
                for i in url_new:
                    t.submit(crawler,i)

            url_all.concat_lists(url_temp.my_list)


    #################url入口点
    # 获取多个链接的信息，可以选择是否启用站点爬虫
    def get_info_of_url_s(self,urls):
        if self.do_crawler:
            self.crawler_info_from_url_s(urls)

        else :
            for url in urls:
                self.base_get_info_of_url(url)
    
    def get_info_of_url(self,url):
        self.get_info_of_url_s([url])

        



    # 获取某个域名或者ip的存活站点，原理：根据host创建一些url，直接丢到爬虫
    def get_website_of_subdomain(self,subdomain):
        urls=list()
        protocol=["http","https"]
        # 端口字典，注意不要把80和443加进去
        port=['','8080','8090','8888','5003']

        # 加载端口字典
        port_dict=mydb().query_sqlite("select distinct port  from port_dict")['result']
        for i in port_dict:
            if i[0] not in port and i[0] not in ['80','443','3389','3306','22']:
                port.append(i[0])

        for i in protocol:
            for j in port:
                if j == '':
                    urls.append(i+"://"+subdomain)
                else:
                    urls.append(i+"://"+subdomain+":"+j)
        # urls.append("https://101.34.85.116:5003/login")
        self.get_info_of_url_s(urls)
        
    # 获取多个域名或者ip的存活站点
    def get_website_of_subdomain_s(self,subdomains):
        # for subdomain in subdomains:
        #     self.get_website_of_subdomain(subdomain)

        with ThreadPoolExecutor(max_workers=300) as executor:
            for subdomain in mylist(subdomains).my_list:
                executor.submit(self.get_website_of_subdomain, subdomain)    




    # 获取ip的信息，包括ip信息和站点
    def get_info_of_ip(self,ip):
        x=myhost(ip)
        db=mydb()
        db.insert_or_update_table("ip",{
                "ip":ip,
                "port":"\t".join(x.get_opening_port())
            })
        self.get_website_of_subdomain(ip)


    #################ips入口点
    # 获取多个ip的信息，包括ip信息和站点
    def get_info_of_ip_s(self,ip_s):
        # for ip in ip_s:
        #     self.get_info_of_ip(ip)
        with ThreadPoolExecutor(max_workers=300) as executor:
            for ip in mylist(ip_s).my_list:
                executor.submit(self.get_info_of_ip, ip)




    # 获取域名的信息，包括子域名，站点，ip信息
    def get_info_of_domain(self,domain):
        x=myhost(domain)
        db=mydb()
        subdomain_and_ip=x.get_subdomain_and_ip()
        subdomain = list()
        ip = list()
        for i in subdomain_and_ip:
            subdomain.append(i)
        for i in subdomain_and_ip:
            ip.append(subdomain_and_ip[i])

        for i in subdomain_and_ip:
            db.insert_or_update_table("subdomain",{
                "subdomain":i,
                "domain":domain,
                "ip":subdomain_and_ip[i]
            })
        
        self.get_website_of_subdomain_s(subdomain)
        self.get_info_of_ip_s(ip)

    #################domains入口点
    # 获取多个域名的信息
    def get_info_of_domain_s(self,domain_s):
        for doamin in domain_s:
            self.get_info_of_domain(doamin)




    # 获取公司的信息
    def get_info_of_company(self,company):
        mylog().info("get info of company {}".format(company))
        icp_of_company = myhost(company).get_icp_info_of_host()
        domain_of_company=list()
        for i in icp_of_company:
            x=mydb()
            x.insert_or_update_table("domain",{"company":company,"icp_licence":i["domain_licence"],"domain":i["domain_name"]})
            domain_of_company.append(i["domain_name"])
        # self.get_info_of_domain_s(domain_of_company)
        for i in domain_of_company:
            if myhost(i).judge_host_is_ip():
                self.get_info_of_ip(i)
            else:
                self.get_info_of_domain(i)


    ##########company入口点
    # 获取多个公司的信息
    def get_info_of_company_s(self,companys):
        for company in companys:
            self.get_info_of_company(company)
        # with ThreadPoolExecutor(max_workers=300) as executor:
        #     for company in mylist(companys).my_list:
        #         executor.submit(self.get_info_of_company, company)
