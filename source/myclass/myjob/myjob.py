from ..mydb import mydb
from ..mylist import mylist
from ..myurl import myurl
from ..myassembly import myassembly
from .dingding import send_message_to_dingding
from .get_key_of_job import get_key_of_job
import time
from source.config import config
# 任务下发
class myjob:
    def __init__(self, target_list=[], describe='', do_crawler=config.do_crawler,id=None) -> None:
        # 传入任务，自动生成 id
        # 传入的参数 : target(list)  describe(str)
        self.do_crawler = do_crawler
        if id == None:
            self.id = self.generate_id()
            self.describe = describe
            self.target_list = mylist(target_list)
            self.company_s = self.target_list.extract_company_from_list()
            self.ip_s = self.target_list.extract_ip_from_list()
            self.domain_s = self.target_list.extract_domain_from_list()
            self.url_s = self.target_list.extract_url_from_list()
            self.all_target = mylist().concat_lists_without_add(
                self.company_s, self.domain_s, self.ip_s, self.url_s)
        else :
            self.id = id
            self.describe = describe
            self.target_list = mylist(
                mydb().query_sqlite(
                    "select target from task where id = {}".format(self.id)
                    )["result"][0][0].split("\t")
                )
            print(self.target_list.my_list)
            self.company_s = self.target_list.extract_company_from_list()
            self.ip_s = self.target_list.extract_ip_from_list()
            self.domain_s = self.target_list.extract_domain_from_list()
            self.url_s = self.target_list.extract_url_from_list()
            self.all_target = mylist().concat_lists_without_add(
                self.company_s, self.domain_s, self.ip_s, self.url_s)


    # 用时间戳生成任务id
    # 对象生成时自动调用
    def generate_id(self):
        time.sleep(0.001)  # 等待1毫秒
        timestamp = int(time.time() * 1000)  # 获取当前时间戳，并将其乘以1000，以保留毫秒级别的精度
        return timestamp

    # 将任务 id，describe，target 写入数据库
    def write_task_to_db(self):
        x = mydb()
        x.insert_or_update_table("task", {
            "id": self.id,
            "describe": self.describe,
            "target": "\t".join(self.all_target)
        }
        )


    #  将数据库内任务的状态标志为已完成，并且写入数据量情况
    def write_done_to_db(self):
        from .write_done_to_db import write_done_to_db
        write_done_to_db(self.id)



    # 开始运行
    def do_job(self):
        self.write_task_to_db()  # 将任务写入数据库
        self.describe = "crawler "+self.describe
        send_message_to_dingding("任务开始!\nid:{}\ntarget:{}".format(self.id,self.all_target))
        myassembly(self.do_crawler).get_info_of_company_s(self.company_s)
        myassembly(self.do_crawler).get_info_of_domain_s(self.domain_s)
        myassembly(self.do_crawler).get_info_of_ip_s(self.ip_s)
        myassembly(self.do_crawler).get_info_of_url_s(self.url_s)
        self.write_done_to_db() #完成后将状态写入数据库


    # 获取任务目标的关键字，用于查询任务的数据
    # 根据id
    def get_key_of_job(self, id) -> list:
        return get_key_of_job(id)


    # 根据id返回数据
    def get_task_data_by_id(self,id)->dict:
        from .get_task_data_by_id import get_task_data_by_id
        return get_task_data_by_id(id)

    # 根据id导出数据
# def save_query_results_to_excel(field_names_list, field_values_list, file_name="query_results.xlsx",pagename=[]):
    def save_data_by_id(self,id,filename="result.xlsx"):
        from .save_file import save_query_results_to_excel
        data = self.get_task_data_by_id(id)
        save_query_results_to_excel(data['field_names'],data['result'],file_name=filename,pagename=data['page_name'])
