# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AutoUpdateApp.py
@time: 2020.1.28 16:28
"""

from AppService import AppService

from tools.Result import *
from tools.Logger import *
from tools.CheckInternet import *

def main():
	logger=Logger("data/log.txt","AutoUpdateApp.py.py",True)
	
	logger.info("开始自动更新:")
	
	if(not isConnected("http://www.baidu.com")):
		logger.error("网络连接超时！\n")
		return
	
	serv=AppService()
			
	res=serv.updateAllApps()
	
	if(not res.equal(ResultEnum.SUCCESS)):
		logger.error("自动更新出错: "+res.toString())
	else:
		logger.info("自动更新完成。\n")
	
if __name__ == "__main__":
	main()
