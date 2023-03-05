
# -*- coding: UTF-8 -*-
import io
import PyPDF2
import requests
import magic
import zipfile
import re
from source.myclass.mylist import mylist
import docx
import pandas as pd
import urllib.parse
import urllib
import os
from bs4 import BeautifulSoup
import socket
from source.myclass.myurl import myurl
from source.myclass.myrequests import myrequests
from source.myclass.mylog import mylog

class myinfoget(myurl,myrequests):
    def __init__(self,url,**kwargs) -> None:
        myurl.__init__(self,url)
        myrequests.__init__(self,url,**kwargs)
        self.url=url
        self.type = self.determine_file_type_to_natural_language(self.response.content,self.url)
        self.text = self.extract_text_from_all_kinds_content(self.response.content,self.type,self.url)

    def determine_file_type_to_natural_language(self,content,url):
        from .determine_file_type_to_natural_language import determine_file_type_to_natural_language
        return determine_file_type_to_natural_language(content,url)


    def extract_text_from_all_kinds_content(self,content,type,url):
        from .extract_text_from_all_kinds_content import extract_text_from_all_kinds_content
        return extract_text_from_all_kinds_content(content,type,url)
    
    # 提取铭感信息
    def get_sensitive_information(self)->dict:
        from .extract_sensitive_infomation import extract_sensitive_infomation
        return extract_sensitive_infomation(self.text,self.url)

    # 提取所有链接
    def get_all_link(self)->list:
        res=re.findall(r"https?://[\w\.\?\/\-\=\~]+",self.text)#包含协议的链接，如"http://baidu.com"

        ur_without_scheme=re.findall(r"(?:\=[\"\']+\/\/)([\w\.\?\/\-\=\~]+)",self.text)#未说明协议的链接,如"src="//baidu.com/""

        the_path=re.findall(r"(?:(?:src=|url=|link=|href=)[\"\']*)(?!http://|https://|//)([\.\w\-\?\=\/\~\:]+)(?:[\"\']*)",self.text)#有时候会提取到伪协议
        # path=re.findall(r"(?:(?:src=|url=|link=|href=)[\"\']*)(?!http://|https://|//)(/[\.\w\-\?\=\/\~\:]+)(?:[\"\']*)",text)
        for i in the_path:
            if re.search(r"\w+:\D",i) or i[-1]==':':#去除path中包含xx:xx的项目
                pass
            else:
                if i[0]=='/':
                    res.append(self.get_base_path()+i)
                #路径是'/js/a.js'
                if i[0]!='/':
                    res.append(self.get_current_path()+'/'+i)
                #路径是'js/a.js'

        for i in ur_without_scheme:
            res.append(self.get_scheme()+i)
        # 处理未包含协议的链接

        the_result=list()
        for i in res:
            if myurl(i).judge_url_is_rigth() and i not in the_result:
                the_result.append(i)
        return the_result

    # 根据关键字提取链接，关键字为列表
    def get_link_by_key(self,key)->list:
        all_link = self.get_all_link()
        key_link = list()
        for link in all_link:
            if key in link:
                key_link.append(link)
        return key_link

    # 根据主机地址提取链接，可以是ip
    def get_link_by_host(self)->list:
        return self.get_link_by_key(self.get_hostname())

    # 根据根域名提取链接
    def get_link_by_domain_root(self)->list:
        return self.get_link_by_key(self.get_domain_root())

    # 提取网站标题
    def get_title(self)->str:
        soup = BeautifulSoup(self.text, 'html.parser')
        try:
            return soup.title.string
        except BaseException:
            message = "get_title fail in url:{}".format(self.url)
            mylog().info(message)
            return ""
