import time
class config:
    # 线程数，根据服务器性能选择合适数量
    works_scan_port = 300
    

    # 是否收集子域名，适合子域名收集完成的情况
    get_subdomain = True
    scan_port = False
 

    # fofa email and api_key
    fofa_email = ""
    fofa_key = ""

    # securitytrails_api_key 一个数据库网站，用于子域名获取
    securitytrails_api_key = ''
    # 启用站点爬虫？true or flase
    do_crawler = True
    
    # 字典目录
    path_subdomain_dict="source/mydict/subdomain.txt"


    # 钉钉webhook和密钥,必须要口令
    secret = ''
    webhook = ''

    # 爬虫深度，太大容易被封
    crawler_depth = 1



    # 关于requests的配置,全局都采用这个,不用就注释掉
    proxies = {
        # 'http': 'http://127.0.0.1:8080'
        # 'https': 'https://127.0.0.1:8080' 
    }
    timeout = 5

    hearders = {
        'Accept': '*',
        'Content-Type': '*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    allow_redirects = True

    # 输出时间

    # 保存当前任务id
    task_id = None
