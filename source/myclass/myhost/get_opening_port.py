from .the_modules import *
from source.myclass.mydb import mydb
from source.config import config

def get_opening_port(host):
    if config.scan_port:
        # 端口扫描的最大线程
        # max_workers=30
        # 端口扫描列表
        ports_will_test = [22,3389,445,3306,1433,1521,21,27017,11211,5432,23,25,465,110,995,143,993,5900,6379]

        port_dict=mydb().query_sqlite("select distinct port  from port_dict")['result']
        for i in port_dict:
            if int(i[0]) not in ports_will_test:
                ports_will_test.append(int(i[0]))

        def scan_port(host, port):
            for i in (1,2,3):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    return (port, result == 0)
                except Exception:
                    pass
            return (port, False)
        open_ports = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port, host , port) for port in ports_will_test]
            for future in as_completed(futures):
                port, status = future.result()
                if status:
                    open_ports.append(str(port))
        return open_ports
    else:
        return []