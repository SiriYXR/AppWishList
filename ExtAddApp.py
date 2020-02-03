# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ExtAddApp.py
@time: 2019.12.25 11:29
"""
import sys
import appex
import console

from AppService import AppService
from ConfigService import ConfigService

from tools.Result import *
from tools.Logger import *

def main(rootpath="data/"):
	logger=Logger(rootpath+"log.txt","ExtAddApp.py",True)
	configService=ConfigService(rootpath)
	
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
		
	url = appex.get_url()
	if not url:
		console.alert("Error","No input URL found.",'OK', hide_cancel_button=True)
		
		if(configService.getLog().getData()==1):
			logger.error("No input URL found.")
		return
	
	console.hud_alert("正在抓取数据，请等待...","success")
		
	appSerVice=AppService(rootpath)	
	res=appSerVice.addApp(url)
		
	if(res.equal(ResultEnum.APP_UPDATE)):
		console.hud_alert("应用更新成功!",'success')
	elif(res.equal(ResultEnum.SUCCESS)):
		console.hud_alert("应用添加成功!",'success')
	else:
		console.hud_alert(res.getInfo(),'error')
	
		
if __name__ == "__main__":	
	main()
