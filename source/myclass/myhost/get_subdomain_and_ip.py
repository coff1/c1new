from .the_modules import *
from source.myclass.mylog import mylog
def get_subdomain_and_ip(domain):   
    res={}
    def get_ip(domain):
        for i in (1,2,3,4):
            try:
                ip = socket.gethostbyname(domain)
                if ip!=None:
                    res[domain]=ip
                    message = "get ip of {} success".format(domain)
                    mylog().info(message)
                return 0
            except BaseException:
                pass
        message = "get ip of {} fail".format(domain)
        mylog().info(message)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        subdomains = get_subdomain(domain)
        mylog().info("resolve {} subdomains of {}".format(len(subdomains),domain))
        for subdomain in subdomains:
            executor.submit(get_ip, subdomain)
    return res
