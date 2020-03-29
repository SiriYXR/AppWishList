# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: ExtAddApp.py
@createTime: 2019.12.25 11:29
@updateTime: 2020-03-29 11:18:31
"""
import sys
import appex
import console
import sys
sys.path.append('.') # 将项目根目录加入模块搜索路径，这样其他模块才能成功导包

from core.AppService import AppService
from core.ConfigService import ConfigService

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
	
	# 选择添加到愿望单还是收藏夹
	star=True
	if(console.alert("添加应用","请选择添加到愿望单还是收藏夹","愿望单","收藏夹", hide_cancel_button=True)==2):
		star=False
		
	console.hud_alert("正在抓取数据，请等待...","success")
		
	appSerVice=AppService(rootpath)	
	res=appSerVice.addApp(url,star)
		
	if(res.equal(ResultEnum.APP_UPDATE)):
		console.hud_alert("应用更新成功!",'success')
	elif(res.equal(ResultEnum.SUCCESS)):
		console.hud_alert("应用添加成功!",'success')
	else:
		console.hud_alert(res.getInfo(),'error')
	
	appex.finish()
		
if __name__ == "__main__":	
	main()
