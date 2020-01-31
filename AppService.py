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
from ConfigService import ConfigService

from tools.GetJson import *
from tools.DownLoadImage import *
from tools.CutImage import *
from tools.Result import *
from tools.Logger import *

class AppService (object):
	
	def __init__(self,rootpath="data/"):
		self.rootpath=rootpath
		
		dbpath=self.rootpath+"database.db"
		self.mAppController=AppController(dbpath)
		self.mPriceService=PriceService(rootpath)
		self.mConfigService=ConfigService(rootpath)
		
		self.logger=Logger(self.rootpath+"log.txt","AppService.py",True)
		
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
		res=self.mPriceService.addPrice(app,jsondic)
		
		# 调用更新时再下载，加快应用添加速度，以免用户长时间等待
		# downLoadImage(app.getImgURL(),"data/img/"+app.getAppId()+".png")
		
		self.logger.info("添加app：\n"+app.toString()+"\n")
		return Result(ResultEnum.SUCCESS,app)
	
	def getAppByAppId(self,appid):
		res=self.mAppController.selectAppByAppId(appid)
		
		if(res==None):
			self.logger.error("通过appid查询失败："+appid)
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
		
	def getAllApps(self):
		res=self.mAppController.selectAllApps()
		
		if(res==None):
			self.logger.error("getAllApps()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
		
	def getAppsByCategory(self,category):
		res=self.mAppController.selectAppsByCategory(category)
		
		if(res==None):
			self.logger.error("getAppsByCategory()"+ResultEnum.SELECT_ERROR[1])			
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
		
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

		res=self.mConfigService.getNotice()
		if(res.isPositive() and res.getData()==1):
			if(not os.path.exists(self.rootpath+"img/"+app.getAppId()+".png")):
				downLoadImage(app.getImgURL(),self.rootpath+"img/"+app.getAppId()+".png")
				cutImage(self.rootpath+"img/"+app.getAppId()+".png",(387,102,813,528))
		
		res=self.mPriceService.addPrice(app,jsondic)
		if(res.equal(ResultEnum.PRICE_NOTICE)):
			notice=self.mConfigService.getNotice()
			if(notice.isPositive() and notice.getData()==1):
				print(res.getInfo())
				self.logger.info(res.getInfo())
		
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
		fault=0
		
		for i in apps:
			res=self.updateApp(i)
			if(res.isPositive()):
				newapps.append(res.getData())
			else:
				fault+=1
			
		return Result(ResultEnum.SUCCESS,(newapps,fault))
	
	def deleteApp(self,app):
		if(app.getId()<0):
			self.logger.warning("deleteApp()"+ResultEnum.APP_INVALID[1])
			return Result(ResultEnum.APP_INVALID)
		
		self.mAppController.deleteAppById(app.getId())
		self.mPriceService.deletePriceByAppId(app.getAppId())
		
		self.logger.warning("deleteApp()删除app："+app.getAppId())
		
		return Result(ResultEnum.SUCCESS)
		
	def deleteAppByAppId(self,appid):
		
		self.mAppController.deleteAppByAppId(appid)
		self.mPriceService.deletePriceByAppId(appid)
		
		self.logger.warning("deleteAppByAppId删除app："+appid)
		
		return Result(ResultEnum.SUCCESS)
		
	def getCategories(self):
		res=self.mAppController.selectCategories()

		if(res==None):
			self.logger.error("getCategories()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
				
		return Result(ResultEnum.SUCCESS,res)
	
	def getPricesByApp(self,app):
		return self.mPriceService.getPricesByAppId(app.getAppId())
	
	
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
			
	if(len(res.getData()[0])>0):
		res=serv.getPricesByApp(res.getData()[0])
		
		if(not res.equal(ResultEnum.SUCCESS)):
			print(res.toString())
		else:
			for i in res.getData(): 
				print(i.toString())
	
