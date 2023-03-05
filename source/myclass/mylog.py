import time
class mylog():
    def __init__(self) -> None:
        pass
    
    def time(self):
        return '\033[92m{}\033[0m'.format(time.strftime('%b %d %Y %H:%M:%S', time.localtime()))
    
    def info(self,message):
        print("{}\033[94m[info]{}\n\033[0m".format(self.time(),message),end="")

    def error(self,message):
        print("{}\033[91m[error]{}\n\033[0m".format(self.time(),message),end="")


# mylog().error("111")