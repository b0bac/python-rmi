# -*- coding:utf-8 -*-


"""
    定义一个模块（单文件插件）的客户端类,及其相关API
"""


#引入依赖库模块
import socket
import base64


#定义全局类型
class RemoteModuleIncludeClient(object):
    """定义RMI客户端类"""
    def __init__(self,ServerIP,ServerPort):
        """创建RMI客户端实例"""
        self.Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.Client.connect((ServerIP,ServerPort))
        except Exception,reason:
            raise Exception(reason)

    def __Authcation(self,username,password):
        """发送身份验证信息"""
        return "%s[RMI-AUTH-USERNAME]--[RMI-AUTH-PASSWORD]%s"%(username,password)

    def Connect(self,username=None,password=None):
        """连接客户端"""
        try:
            while True:
                data = self.Client.recv(1024)
                if data == "RMI-STATUS-00":
                    break
                elif data == "RMI-STATUS-02":
                    raise Exception("连接异常!")
                elif "RMI-STATUS-01" in data:
                    self.Client.send(self.__Authcation(username,password))
                elif "RMI-STATUS-03" in data:
                    raise Exception("客户端未验证!")
                elif "RMI-STATUS-04" in data:
                    raise Exception("请求模块不存在")
        except Exception,reason:
            print "[-] 连接异常"
            raise

    def GetModuleCode(self,ModuleName):
        """获取模块代码"""
        try:
            self.Client.send(ModuleName)
            code = self.Client.recv(4096)
            return base64.b64decode(code)
        except Exception:
            raise
