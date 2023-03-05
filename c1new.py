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
parser.add_argument("--delete","-d",help="--delete all 删除任务列表(数据保存)")
args=parser.parse_args()


if args.target:
    if 'txt' in args.target:
        target_list = mylist().read_list(args.target)
        myjob(target_list).do_job()
    elif len(args.target) == 13:
        target_id = int(args.target)
        myjob(id=target_id).do_job()
    else:
        myjob([args.target]).do_job()

if args.id and args.output:
    myjob().save_data_by_id(args.id,filename=args.output)

if args.show:
    result = mydb().query_sqlite("select * from task order by id")["result"]
    for i in result:
        for j in i :
            print(" {} ".format(j),end='')
        print('')

if args.delete:
    if args.delete == "all":
        mydb().execute_sqlite("delete from task")
        mylog().info("成功删除任务列表")