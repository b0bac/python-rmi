# -*- coding:utf-8 -*-


"""
    定义一个仓库对外提供服务的网络接口
"""


#引入依赖库模块
import socket
import select
from Repertory import *


#定义全局类型
class RemoteModuleIncludeServer(object):
    """定义RMI服务类"""
    def __init__(self,RepertoryPath,LocolIP,LocalPort):
        """创建RMI服务器实例"""
        self.ModuleRegister = ModuleRepertory(RepertoryPath)
        self.Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Server.bind((LocolIP,LocalPort))
        self.ClientRegisterList = []
        self.AuthFlag = False
        self.Username = None
        self.Password = None
        self.ReadSocket = [self.Server]
        self.WriteSocket = []
        self.ErrorSocket = [self.Server]

    def SetAuthConfig(self,flag,username=None,password=None):
        """设置认证"""
        if flag == True:
            if isinstance(username,str) and isinstance(password,str):
                raise Exception("认证参数存在类型类型")
            else:
                self.AuthFlag = True
                self.Username = username
                self.Password = password
        else:
            pass

    def ServiceListen(self,AsyncNumber):
        """配置服务开启监听"""
        print "[+] 服务配置监听:",AsyncNumber
        try:
            self.Server.listen(AsyncNumber)
        except Exception,reason:
            raise Exception(reason)

    def StartService(self):
        """启动服务"""
        print "[+] 服务启动"
        while True:
            readlist,writelist,errorlist = select.select(self.ReadSocket,self.WriteSocket,self.ErrorSocket)
            for sockfd in readlist:
                if sockfd == self.Server:
                    client,addr = sockfd.accept()
                    if client not in self.ClientRegisterList:
                        if self.AuthFlag:
                            try:
                                client.send("RMI-STATUS-01")
                                data = client.recv(1024)
                            except Exception,reason:
                                continue
                            user = str(data).split("[RMI-AUTH-USERNAME]")[0]
                            pswd = str(data).split("[RMI-AUTH-PASSWORD]")[-1]
                            if user == self.Username and pswd == self.Password:
                                try:
                                    client.send("RMI-STATUS-00")
                                except Exception,reason:
                                    continue
                                self.ClientRegisterList.append(client)
                                self.ReadSocket.append(client)
                                self.ErrorSocket.append(client)
                            else:
                                client.send("RMI-STATUS-02")
                                continue
                        else:
                            client.send("RMI-STATUS-00")
                            self.ClientRegisterList.append(client)
                            self.ReadSocket.append(client)
                            self.ErrorSocket.append(client)
                    else:
                        self.ReadSocket.append(client)
                        self.ErrorSocket.append(client)
                else:
                    data = sockfd.recv(4096)
                    if data == "":
                        self.ReadSocket.remove(sockfd)
                        self.ErrorSocket.remove(sockfd)
                        self.ClientRegisterList.remove(sockfd)
                    if sockfd not in self.ClientRegisterList:
                        sockfd.send("RMI-STATUS-03")
                        continue
                    if data in self.ModuleRegister.ModuleRegisterDictionary:
                        code = self.ModuleRegister.ModuleGetCode(data)
                        if code != None:
                            sockfd.send(code)
                    else:
                        sockfd.send("RMI-STATUS-04")
