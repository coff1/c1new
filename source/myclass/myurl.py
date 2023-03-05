# -*- coding: UTF-8 -*-
import re
import urllib.parse
import urllib
from .myhost import myhost
from .mylog import mylog
class myurl(myhost):
    def __init__(self,url) -> None:
        self.url=url
        self.parsed_url=urllib.parse.urlsplit(self.url)
        myhost.__init__(self,self.get_hostname())

    def get_hostname(self):
        return "{0.hostname}".format(self.parsed_url)

    def get_netloc(self):
        return "{0.netloc}".format(self.parsed_url)

    def get_base_path(self):
        path = "{0.scheme}://{0.netloc}".format(self.parsed_url)
        if path.endswith("/"):
            path = path[:-1]
        return path

    def get_current_path(self):
        path="{0.scheme}://{0.netloc}{0.path}".format(self.parsed_url)
        if path.endswith("/"):
            path = path[:-1]
        return path

    def get_scheme(self):
        return self.parsed_url.scheme

    def judge_host_is_ip(self):
        pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(pattern, self.get_hostname()) is not None
    
    def get_port_from_url(self):
        port=self.parsed_url.port
        if port ==None:
            if self.get_scheme() == "http":
                port = 80
            if self.get_scheme() == "https":
                port = 443
        return port

    def judge_url_is_rigth(self):
        pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(pattern, self.url) is not None


    # 当爬取ip站点或域名无法提取时返回host
    def get_domain_root(self):
        res=re.findall(r"([\w\-]+(?:.com.cn|.com|.edu.cn|.edu|.gov.cn|.gov|.info.cn|.info|.biz.cn|.biz|.co.cn|.co|.uk.cn|.uk|.us.cn|.us|.net.cn|.net|.org.cn|.org|.cn))",self.url)
        try:
            return res[0]
        except BaseException:
            message = "my error on myurl.get_domain_root:can't get url's domain_root , i will return the host  {}".format(self.url)
            mylog().info(message)
            return self.get_hostname()
    
    #获取域名    
    def get_domain(self):
        if self.judge_host_is_ip() == False:
            return self.get_hostname()
        message = "myurl.get_domain: get_domain of {} fail".format(self.url)
        mylog().info(message)
        

