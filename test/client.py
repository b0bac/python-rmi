# -*- coding:utf-8 -*-
import sys
sys.path.append("../")
from rmi.Client import RemoteModuleIncludeClient as Client


if __name__ == "__main__":
    client = Client("127.0.0.1",12345)
    client.Connect()
    data = client.GetModuleCode("test")
    exec(data)
    s1 = Student("Tom")
    s1.show()
