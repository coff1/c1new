from source.myclass import myjob
from source.myclass import mylist
from source.myclass import mydb
from source.config import config
from source.myclass.mylog import mylog

print("""
 _______  __    _        _______          
(  ____ \/  \  ( (    /|(  ____ \|\     /|
| (    \/\/) ) |  \  ( || (    \/| )   ( |
| |        | | |   \ | || (__    | | _ | |
| |        | | | (\ \) ||  __)   | |( )| |
| |        | | | | \   || (      | || || |
| (____/\__) (_| )  \  || (____/\| () () |
(_______/\____/|/    )_)(_______/(_______)
https://github.com/coff1/c1new
{}
""".format(mylog().time()))


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--target","-t",help="目标,可以是id或txt文件或单个目标字符串")
parser.add_argument("--id","-i",help="指定id,和output连用输出结果")
parser.add_argument("--output","-o",help="输出文件")
parser.add_argument("--show","-s",help="--show all 显示任务列表")
parser.add_argument("--delete","-d",help="task 删除任务列表(数据保存) all 删除所有数据")
parser.add_argument("--do_crawler","-crawler",help="是否启用站点爬虫,默认为False",default=False,type=bool)
parser.add_argument("--crawler_depth","-depth",help="站点爬虫深度，若为1就是存活检测，默认为1",default=1,type=int)
parser.add_argument("--get_subdomain","-subdomain",help="是否进行子域名收集，适合目标为子域名的情况，默认为False",default=False,type=bool)
parser.add_argument("--scan_port","-port",help="是否进行端口扫描 默认False",default=False,type=bool)
args=parser.parse_args()


if args.get_subdomain:
    config.get_subdomain = True
else:
    config.get_subdomain = False

if args.do_crawler:
    config.do_crawler = True
else:
    config.do_crawler = False

if args.scan_port:
    config.scan_port = True
else:
    config.scan_port = False


config.crawler_depth = int(args.crawler_depth)

print(f"""
get_subdomain\t{config.get_subdomain}
do_crawler\t{config.do_crawler}
crawler_depth\t{config.crawler_depth}
scan_port\t{config.scan_port}
""")
      

import time


if args.target:
    time.sleep(2)
    if 'txt' in args.target:
        target_list = mylist().read_list(args.target)
        myjob(target_list).do_job()
    elif len(args.target) == 13:
        target_id = int(args.target)
        myjob(id=target_id).do_job()
    else:
        myjob([args.target]).do_job()

# if args.id and args.output:
#     myjob().save_data_by_id(args.id,filename=args.output)

# 保存文件，默认文件名为id名
if args.id:
    config.task_id = int(args.id)

if config.task_id:
    if args.output:
        myjob().save_data_by_id(config.task_id,filename=args.output)
    
    else:
        myjob().save_data_by_id(config.task_id,filename=str(config.task_id)+".xlsx")


if args.show:
    result = mydb().query_sqlite("select * from task order by id")["result"]
    for i in result:
        for j in i :
            j=str(j).replace("\t",",")
            if len(str(j))>100:
                j=str(j)[:100]+"......"
            print(" {} ".format(j),end='')
        print('')

if args.delete:
    if args.delete == "task":
        mydb().execute_sqlite("delete from task")
        mylog().info("成功删除任务列表")
    
    if args.delete == "all":
        mydb().execute_sqlite("delete from domain")
        mydb().execute_sqlite("delete from ip")
        mydb().execute_sqlite("delete from sensitiveinfo")
        mydb().execute_sqlite("delete from subdomain")
        mydb().execute_sqlite("delete from task")
        mydb().execute_sqlite("delete from url")
        mylog().info("成功删除所有数据")