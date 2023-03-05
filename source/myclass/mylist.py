import re
class mylist:
    def __init__(self,*lists) -> None:
        self.my_list_out=list()
        self.my_list=list()
        self.my_list = self.concat_lists(*lists)

    def read_list(self,filename):
        f=open(filename,encoding="utf-8")
        for i in f.readlines():
            if i.strip() not in self.my_list:
                self.my_list.append(i.strip())
        return self.my_list

    def save_list(self,filename):
        f = open(filename,"w",encoding="utf-8")
        for i in self.my_list:
            f.write(str(i)+"\n")
        f.close()
        return self.my_list


    def concat_lists(self,*lists):
        result = []
        for lst in lists:
            if lst !=None:
                result += lst
        for i in result:
            if i not in self.my_list:
                self.my_list.append(i)
        return self.my_list

    def concat_lists_without_add(self,*lists):
        result = []
        for lst in lists:
            if lst !=None:
                result += lst
        return result

    def add_one_to_list(self,the_one_to_add):
        if the_one_to_add not in self.my_list:
            self.my_list.append(the_one_to_add)

    
    def print_list(self):
        for i in self.my_list:
            print(i)
        return self.my_list

    def get_length(self):
        return len(self.my_list)

    # 模仿队列
    def out_one_from_list(self):
        the_out_one = self.my_list[len(self.my_list_out)]
        self.my_list_out.append(the_out_one)
        return the_out_one


    def get_my_list_new(self):
        my_list_new=list()
        for i in self.my_list:
            if i not in self.my_list_out:
                my_list_new.append(i)
        return my_list_new

    def extract_ip_from_list(self,*input_list):
        self.concat_lists(*input_list)
        ip_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        return [item for item in self.my_list if re.match(ip_pattern, item)]


    def extract_url_from_list(self,*input_list):
        self.concat_lists(*input_list)
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        def judge_is_url(text):
            match = re.findall(url_pattern,text)
            if match:
                if match[0]==text:
                    return 1
            return 0
        return [item for item in self.my_list if judge_is_url(item)]

    def extract_company_from_list(self,*input_list):
        self.concat_lists(*input_list)
        return [item for item in self.my_list if "公司" in item]


    def extract_domain_from_list(self,*input_list):
        self.concat_lists(*input_list)
        domain_pattern = r'[\w\-\.]+\.[a-zA-Z]+'
        def judge_is_domain(text):
            match = re.findall(domain_pattern,text)
            if match:
                if match[0]==text:
                    return 1
            return 0
        return [item for item in self.my_list if judge_is_domain(item)]



# if __name__ == "__main__":
#     x=mylist()
#     print(x.extract_ip_from_list(["1.1.1.1","http://192.168.1.1:8000"]))
#     print(x.out_one_from_list())
#     print(x.get_my_list_new())