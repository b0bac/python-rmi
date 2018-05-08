# -*- coding:utf-8 -*-
import sys
sys.path.append("../")
from rmi.Server import RemoteModuleIncludeServer as Server


if __name__ == "__main__":
    server = Server("./tmp","127.0.0.1",12345)
    server.ServiceListen(5)
    server.ModuleRegister.ModuleAppend("test.py")
    server.StartService()
