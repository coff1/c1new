from .the_modules import *
from source.myclass.mylog import mylog
class myhost:
    def __init__(self,host) -> None:
        self.host = host

    # 获取主机域名，当host不为域名形式时不能使用
    def get_domain_root(self):
        res=re.findall(r"([\w\-]+(?:.com.cn|.com|.edu.cn|.edu|.gov.cn|.gov|.info.cn|.info|.biz.cn|.biz|.co.cn|.co|.uk.cn|.uk|.us.cn|.us|.net.cn|.net|.org.cn|.org|.cn))",self.host)
        try:
            return res[0]
        except BaseException:
            message="my error on myurl.get_domain_root:can't get url's domain_root i will return the host {}".format(self.host)
            mylog().error(message)
            return self.host
        
    def judge_host_is_ip(self):
        pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(pattern, self.host) is not None
    
    # 获取主机ip
    def get_host_ip(self):
        try:
            socket.setdefaulttimeout(5)
            host_ip = socket.gethostbyname(self.host)
            return host_ip
        except BaseException:
            message = "my error in myurl.get_host_ip:can't get host's ip  {}".format(self.host)
            mylog().info(message)

    # 获取ipc备案信息
    def get_icp_info_of_host(self)->str:
        return icp_checker(self.host)

    # 端口扫描
    def get_opening_port(self)->list:
        return get_opening_port(self.host)

    # 获取子域名
    def get_subdomain(self)->list:
        return get_subdomain(self.host)

    
    def get_subdomain_and_ip(self)->dict:
        return get_subdomain_and_ip(self.host)



    
if __name__ == "__main__":
    pass
