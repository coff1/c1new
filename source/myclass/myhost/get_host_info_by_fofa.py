from .the_modules import *
from source.config import config
from source.myclass.mylog import mylog
# fofa信息查询

def get_host_info_by_fofa(host):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        grammar = "domain=" + '"' + host + '"'
        encoded_grammar = base64.b64encode(grammar.encode()).decode()
        url = "https://fofa.info/api/v1/search/all?size=10000&email={}&key={}&qbase64={}".format(config.fofa_email,config.fofa_key,encoded_grammar)
        response = requests.get(url,headers=headers)
        data = response.text
        data = json.loads(data)
        subdomains = list({re.findall(r"(?://)?([\w\-\.]+)(?::)?", i[0])[0] for i in data["results"]})
        ports = list({i[2] for i in data["results"]})

        # 扩充端口字典，可注释掉
        from source.myclass.mydb import mydb
        for i in ports:
            mydb().insert_or_update_table('port_dict',{'port':i})

        # 扩充子域名字典
        for i in subdomains:
            j = i.replace(host,'')
            j = j.strip('.')
            mydb().insert_or_update_table('subdomain_dict',{'subdomain':j})

        return {"subdomains": subdomains, "ports": ports}
    except BaseException:
        try:
            message1 = data
        except BaseException:
            message1 = 'fofa 无返回数据'
            pass
        message = "get_domain_info_by_fofa fail: {} ,checke config or network\n{}".format(host,message1)
        mylog().error(message)
        return {"subdomains": [], "ports": []}
