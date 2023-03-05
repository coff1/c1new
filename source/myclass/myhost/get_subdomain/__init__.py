from source.myclass.myhost.the_modules import *
from source.myclass.mylog import mylog
from .get_subdomain_bing import get_subdomains_bing
# 检验域名合法性
def validate_domains(domains)->list:
    pattern = re.compile(r'^(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}$')
    validated_domains = set()
    for domain in domains:
        if pattern.match(domain):
            validated_domains.add(domain)
    return list(validated_domains)

def get_subdomain(domain)->list:
    # 获取子域名，包含爆破方式
    def get_subdomain_by_brute(domain)->list:
        dns_servers=None
        max_workers=1000
        subdomains = set()
        subdomains_list=mylist().read_list(config.path_subdomain_dict)
        # subdomains_list = ["www", "mail", "ftp", "api", "admin"]
        impossible_subdomains_list = ["qhwfo.iqwj.ofqoiw","ak.aksd.lxmfcsam","wbdq.jfjiq.iko","vsss_ax.aasc","sacSRBHOxxA4F4AVAV","AZAKSNxxFOPP","asdfghtgfvcxxwsxcijhbg"]
        # Use default DNS servers if none are specified
        if not dns_servers:
            resolver = dns.resolver.Resolver()
        else:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = dns_servers

        def resolve_subdomain(subdomain):
            try:
                answers = resolver.resolve(subdomain, "A")
                for rdata in answers:
                    subdomains.add(subdomain)
            except BaseException:
                message  = "resolve_subdomain fail :{}".format(subdomain)
                mylog().info(message)
                pass
        
        #判断是否被泛解析
        impossible_subdomains_to_resolve = ["{}.{}".format(subdomain, domain) for subdomain in impossible_subdomains_list]
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(resolve_subdomain, subdomain) for subdomain in impossible_subdomains_to_resolve]
            concurrent.futures.wait(futures)
        if len(subdomains) > 0:
            message = "域名被泛解析 : {} {}/{}".format(domain, len(subdomains), len(impossible_subdomains_list))
            mylog().error(message)
            return []
        # Generate list of subdomains to resolve
        subdomains_to_resolve = ["{}.{}".format(subdomain, domain) for subdomain in subdomains_list]

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(resolve_subdomain, subdomain) for subdomain in subdomains_to_resolve]
            concurrent.futures.wait(futures)

        return(list(subdomains))

    def get_subdoamin_by_securitytrails(domain):
        subdomains = []
        try:
            # 爬取securitytrails.com的信息
            url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
            headers = {"APIKEY": config.securitytrails_api_key, "Accept": "application/json"}
            params = {"children_only": "false", "include_inactive": "true"}
            resp = requests.get(url, params=params, headers=headers)
            data = json.loads(resp.text)
            for subdomain in data["subdomains"]:
                subdomain = f"{subdomain}.{domain}"
                if f"{domain}." not in subdomain:
                    subdomains.append(subdomain)
        except BaseException:
            message = "获取securitytrails.com的信息失败"
            mylog().error(message)
        return subdomains

    def get_subdoamin_by_rapiddns(domain):
        subdomains = []
        try:
            # 爬取rapiddns.io的信息
            url = f"https://rapiddns.io/subdomain/{domain}?full=1"

            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "lxml")

            for line in soup.text.split("\n"):
                if domain in line and "RapidDNS" not in line and f"{domain}." not in line and line not in subdomains:
                    subdomains.append(line)
        except BaseException:
            message = "获取rapiddns.com的信息失败"
            mylog().error(message)
        return subdomains

    subdomains = mylist(
            get_subdoamin_by_securitytrails(domain),
            get_subdoamin_by_rapiddns(domain),
            get_host_info_by_fofa(domain)["subdomains"],
            get_subdomain_by_brute(domain),
            get_subdomains_bing(domain)["subdomains"]
    ).my_list

    subdomains  = validate_domains(subdomains)

    mylog().info("get {} subdomains of {}".format(len(subdomains),domain))

    return subdomains