# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppService.py
@time: 2019.12.25 09:56
"""
import os
import json

from AppModel import App
from PriceModel import Price
from AppController import AppController
from PriceService import PriceService

from tools.GetJson import *
from tools.DownLoadImage import *
from tools.CutImage import *
from tools.Result import *
from tools.Logger import *

class AppService (object):
	
	logger=Logger("data/log.txt","AppService.py",True)
	
	mAppController = None
	mPriceService = None
	
	def __init__(self):
		self.mAppController=AppController("data/database.db")
		self.mPriceService=PriceService()
		
	def __del__(self):
		pass
		
	def addApp(self,url):
		app=App(url)
		
		jsontxt=GetJson(url)
		
		if(jsontxt == None):
			self.logger.error("jsontxt获取失败："+url)
			return Result(ResultEnum.URL_INVALID)
		
		jsondic=json.loads(jsontxt)

		if(not IsJsonValid(jsondic)):
			self.logger.error("无效json："+url)
			return Result(ResultEnum.URL_INVALID)
			
		app.initByJson(jsondic)
		
		if(self.isExist(app)):
			self.logger.error("app已经存在："+url)
			return Result(ResultEnum.APP_EXIST)
		
		self.mAppController.insertApp(app)
		price=self.mPriceService.addPrice(app,jsondic).getData()
		
		# 调用更新时再下载，加快应用添加速度，以免用户长时间等待
		# downLoadImage(app.getImgURL(),"data/img/"+app.getAppId()+".png")
		
		self.logger.info("添加app：\n"+app.toString()+"\n")
		return Result(ResultEnum.SUCCESS,(app,price))
	
	def getAppByAppId(self,appid):
		res=self.mAppController.selectAppByAppId(appid)
		
		if(res==None):
			self.logger.error("通过appid查询失败："+appid)
			return Result(ResultEnum.SELECT_ERROR)
		
		app=App()
		app.initByTuple(res)
		
		return Result(ResultEnum.SUCCESS,app)
		
	def getAllApps(self):
		res=self.mAppController.selectAllApps()
		
		if(res==None):
			return Result(ResultEnum.SELECT_ERROR)
			
		apps=[]
		
		for i in res:
			a=App()
			a.initByTuple(i)
			apps.append(a)
		
		return Result(ResultEnum.SUCCESS,apps)		
		
	def updateApp(self,app):		
		jsontxt=GetJson(app.getURL())
		
		if(jsontxt == None):
			self.logger.error("jsontxt获取失败："+app.getURL())
			return Result(ResultEnum.URL_INVALID)
		
		jsondic=json.loads(jsontxt)

		if(not IsJsonValid(jsondic)):
			self.logger.error("无效json："+app.getURL())
			return Result(ResultEnum.URL_INVALID)
			
		app.initByJson(jsondic)
		
		self.mAppController.updateApp(app)
		price=self.mPriceService.addPrice(app,jsondic).getData()
		
		if(not os.path.exists("data/img/"+app.getAppId()+".png")):
			downLoadImage(app.getImgURL(),"data/img/"+app.getAppId()+".png")
			cutImage("data/img/"+app.getAppId()+".png",(387,102,813,527))
		
		self.logger.info("更新app："+app.getAppId())
		return Result(ResultEnum.SUCCESS,app)
		
	def updateAppByAppId(self,appid):
		res=self.getAppByAppId(appid)
		
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
		else:
			return self.updateApp(res.getData())
		
	def updateAllApps(self):
		res=self.getAllApps()
		
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
		
		apps=res.getData()
		newapps=[]
		
		for i in apps:
			res=self.updateApp(i)
			if(not res.equal(ResultEnum.SUCCESS)):
				return res
			newapps.append(res.getData())
	
		return Result(ResultEnum.SUCCESS,newapps)
	
	def deleteApp(self,app):
		if(app.getId<0):
			return Result(ResultEnum.INVALID_APP)
		
		self.mAppController.deleteAppById(app.getId())
		self.mPriceService.deletePriceByAppId(app.getAppId())
		
		self.logger.warning("删除app："+app.getAppId())
		
		return Result(ResultEnum.SUCCESS)
		
	def deleteAppByAppId(self,appid):
		
		self.mAppController.deleteAppByAppId(appid)
		self.mPriceService.deletePriceByAppId(appid)
		
		self.logger.warning("删除app："+appid)
		
		return Result(ResultEnum.SUCCESS)
		
	def isExist(self,app):
		if(self.mAppController.selectAppByAppId(app.getAppId()) != None):
			return True
		else:
			return  False

if __name__ == "__main__":
	serv=AppService()
	
	res=serv.getAllApps()
	
	if(res.equal(ResultEnum.SUCCESS)):
		for i in res.getData():
			print(i.toString()+"\n")
			
	res=serv.updateAllApps()
	
	if(not res.equal(ResultEnum.SUCCESS)):
		print(res.toString())
	else:
		print("更新完成。")
			
