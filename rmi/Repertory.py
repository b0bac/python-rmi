# -*- coding:utf-8 -*-


"""
    定义一个Python模块（单文件插件）的仓库类,及其相关API
"""


#引入依赖库模块
import os
import base64


#定义全局类型
class ModuleRepertory(object):
    """模块（单文件插件）仓库类"""
    def __init__(self,path):
        """创建仓库实例"""
        self.ModuleRegisterDictionary = {}
        self.BaseFolder = path
        if self.BaseFolder[-1] != '/':
            self.BaseFolder += '/'
    def __FileFind(self,ModuleName):
        """搜索模块文件是否存在"""
        if self.BaseFolder != None:
            return os.path.exists(self.BaseFolder+ModuleName)
        else:
            return False
    def ModuleAppend(self,FileName):
        """添加模块（单文件插件）"""
        ModuleFileExists = self.__FileFind(FileName)
        if ModuleFileExists:
            ModuleFilePath = self.BaseFolder + FileName
            ModuleName = FileName.split(".py")[0]
            self.ModuleRegisterDictionary[ModuleName] = ModuleFilePath
        return ModuleFileExists
    def ModuleRemove(self,ModuleName):
        """删除模块（单文件插件）"""
        try:
            self.ModuleRegisterDictionary.pop(ModuleName)
        except Exception,reason:
            raise
    def IsModuleAppended(self,ModuleName):
        """判断是否已经添加"""
        if ModuleName in self.ModuleRegisterDictionary:
            return True
        else:
            return False
    def ModuleUpdate(self,ModuleName):
        """更新已经注册的模块（单文件插件）"""
        if self.IsModuleAppended(ModuleName):
            return self.ModuleAppend(ModuleName)
        else:
            return False
    def ModuleGetCode(self,ModuleName):
        """获取注册模块的代码"""
        try:
            ModuleFile = self.ModuleRegisterDictionary[ModuleName]
        except Exception,reason:
            return None
        with open(ModuleFile,"r") as fr:
            code = fr.read()
        try:
            return base64.b64encode(code)
        except Exception,reason:
            return None
