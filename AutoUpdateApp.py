# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: AutoUpdateApp.py
@createTime: 2020.1.28 16:28
@updateTime: 2020-03-29 11:18:44
"""

import sys
sys.path.append('.') # 将项目根目录加入模块搜索路径，这样其他模块才能成功导包

from core.AppService import AppService
from core.ConfigService import ConfigService

from tools.Result import *
from tools.Logger import *
from tools.CheckInternet import *

def main(rootpath="data/"):
	logger=Logger(rootpath+"log.txt","AutoUpdateApp.py.py",True)
	configService=ConfigService(rootpath)
	
	if(configService.getLog().getData()==1):
		logger.info("开始自动更新:")
	
	if(not isConnected("http://www.baidu.com")):
		if(configService.getLog().getData()==1):
			logger.error("网络连接超时！\n")
		return
	
	serv=AppService(rootpath)
			
	res=serv.updateAllApps()
	
	if(not res.equal(ResultEnum.SUCCESS)):
		if(configService.getLog().getData()==1):
			logger.error("自动更新出错: "+res.toString())
	else:
		if(configService.getLog().getData()==1):
			logger.info("自动更新完成。\n")
	
if __name__ == "__main__":
	main("data/")
