# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ExtAddApp.py
@time: 2019.12.25 11:29
"""

import appex
from AppService import AppService
from AppModel import App
from tools.Result import *
from tools.Logger import *
import console

def main():
	logger=Logger("data/log.txt","ExtAddApp.py",True)
	
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
		
	url = appex.get_url()
	if not url:
		console.alert("Error","No input URL found.",'OK', hide_cancel_button=True)
		logger.error("No input URL found.")
		return
		
	serv=AppService()
	res=serv.addApp(url)
	if(res.equal(ResultEnum.SUCCESS)):
		console.alert("Success","应用添加成功!",'OK', hide_cancel_button=True)
	else:
		console.alert("Error",res.getInfo(),'OK', hide_cancel_button=True)
		
if __name__ == "__main__":	
	main()
