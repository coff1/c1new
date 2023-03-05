
import requests
from bs4 import BeautifulSoup
import re
from source.myclass.mylist import mylist
from source.myclass.mylog import mylog

def get_subdomains_bing(domain, num_pages=8):
    try:
        subdomains = []
        urls = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        for i in range(num_pages):
            start_index = i * 10
            url = f'https://www.bing.com/search?q=site%3A{domain}&qs=n&form=QBRE&sp=-1&pq=site%3A{domain}&sc=0-0&sk=&cvid=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&first={start_index}'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            h2_tags = soup.find_all('h2')
            for h2 in h2_tags:
                if h2.a:
                    subdomain_url = h2.a['href']
                    subdomain = re.search('(?<=://)([^/]+)', subdomain_url).group(0)
                    subdomains.append(subdomain)
                    urls.append(subdomain_url)
        subdomains = mylist(subdomains).my_list
        urls = mylist(urls).my_list

        return {"subdomains":subdomains, "urls":urls}
    except BaseException:
        message = "get subdomain from bing fail: {}".format(domain)
        mylog().error(message)
        return {"subdomains":[], "urls":[]}

if __name__ =="__main__":
    subdomains = get_subdomains_bing('usc.edu.cn')
    print(subdomains)