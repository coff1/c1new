from source.myclass.myinfoget import myinfoget
from source.myclass.myassembly import myassembly

url="https://www.usc.edu.cn/images/2023nihaoxinxueqi.jpg"

print(myinfoget(url).type)

myassembly().base_get_info_of_url(url)
    