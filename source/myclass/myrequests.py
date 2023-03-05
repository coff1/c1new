
# -*- coding: UTF-8 -*-
import requests
from source.config import config
class myrequests:
    def __init__(self,url,**kwargs) -> None:
        self.requests_config  = {
            'proxies':config.proxies,
            'timeout':config.timeout,
            'headers':config.hearders,
            'url':url,
            'allow_redirects':config.allow_redirects
        }

        self.method = 'get'

        for i in kwargs:
            if i != 'method':
                self.requests_config[i]=kwargs[i]
            if i == 'method':
                self.method = kwargs[i]


        requests.packages.urllib3.disable_warnings()


        if self.method == "get":
            self.response = requests.get(**self.requests_config)

        if self.method == "post":
            self.response = requests.post(**self.requests_config)

        if self.method == "put":
            self.response = requests.put(**self.requests_config)
        pass


        self.length=len(self.response.content)

        self.content=self.response.content
    
        self.status_code=self.response.status_code
