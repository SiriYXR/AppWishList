# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: AppService.py
@createTime: 2019.12.25 09:56
@updateTime: 2020-03-29 10:53:48
"""

import os
import json

from .AppModel import App
from .PriceModel import Price
from .AppController import AppController
from .PriceService import PriceService
from .ConfigService import ConfigService

from tools.GetJson import *
from tools.DownLoadImage import *
from tools.CutImage import *
from tools.Notification import *
from tools.Result import *
from tools.Logger import *

class AppService (object):
	
	def __init__(self,rootpath="../data/"):
		self.rootpath=rootpath
		
		dbpath=self.rootpath+"database.db"
		self.mAppController=AppController(dbpath)
		self.mPriceService=PriceService(rootpath)
		self.mConfigService=ConfigService(rootpath)
		
		self.mNotification=Notification("AppWishList")
		
		self.logger=Logger(self.rootpath+"log.txt","AppService.py",True)
		
	def __del__(self):
		pass
		
	def addApp(self,url,star=True):
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
			res=self.updateApp(app)
			if (res.equal(ResultEnum.SUCCESS)):
				return Result(ResultEnum.APP_UPDATE)
			return res 
		
		self.mAppController.insertApp(app)		
		self.mPriceService.addPrice(app,jsondic)
		
		# 默认开启自动更新，并设置为愿望单
		app=self.getAppByAppId(app.getAppId()).getData()
		if(star):
			self.starApp(app)
			self.changeAppAutoUpdate(app,1)
		else:
			self.changeAppAutoUpdate(app,0)
		
		# 调用更新时再下载，加快应用添加速度，以免用户长时间等待
		# downLoadImage(app.getImgURL(),"data/img/"+app.getAppId()+".png")
		
		self.logger.info("添加app：\n"+app.toString()+"\n")
		return Result(ResultEnum.SUCCESS,app)
	
	def getAppByAppId(self,appid):
		res=self.mAppController.selectAppByAppId(appid)
		
		if(res==None):
			self.logger.error("通过appid查询失败："+str(appid))
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
		
	def getAllApps(self,where=""):
		res=self.mAppController.selectAllApps(where)
		
		if(res==None):
			self.logger.error("getAllApps()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
		
	def getAppsByCategory(self,category,key=0,desc=0):
		keys=["createtime","name","price"]
		descs=["","DESC"]
		order="ORDER BY "+keys[key]+" "+descs[desc]
		
		if(key==2):
			res=self.mAppController.selectAppsByCategoryOrderByNewestPrice(category,order)
		else:
			res=self.mAppController.selectAppsByCategory(category,order)
		
		if(res==None):
			self.logger.error("getAppsByCategory()"+ResultEnum.SELECT_ERROR[1])			
			return Result(ResultEnum.SELECT_ERROR)
		
		return Result(ResultEnum.SUCCESS,res)
	
	def getAppsByStar(self):
		res=self.mAppController.selectAppsByStar()
		
		if(res==None):
			self.logger.error("getAppsByStar"+ResultEnum.SELECT_ERROR[1])			
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
			
		app.updateByJson(jsondic)
		
		self.mAppController.updateApp(app)
		self.logger.info("更新app："+app.getAppId())
		
		res=self.mConfigService.getNotice()
		if(res.isPositive() and res.getData()==1):
			if(not os.path.exists(self.rootpath+"img/"+app.getAppId()+".png")):
				downLoadImage(app.getImgURL(),self.rootpath+"img/"+app.getAppId()+".png")
				cutImage(self.rootpath+"img/"+app.getAppId()+".png",(387,102,813,528))
		
		res=self.mPriceService.addPrice(app,jsondic)
		
		if(app.getStar() and res.isPositive()):
			notice=self.mConfigService.getNotice()
			if(notice.isPositive() and notice.getData()==1):
				self.noticePrice(app)
				
		return Result(ResultEnum.SUCCESS,app)
		
	def updateAppByAppId(self,appid):
		res=self.getAppByAppId(appid)
		
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
		else:
			return self.updateApp(res.getData())
		
	def updateAllApps(self):
		res=self.getAllApps("WHERE autoupdate=1")
		
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
	
	def updateAllApps_Syn(self,syn=None):
		res=self.getAllApps("WHERE autoupdate=1")
		
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
		
		apps=res.getData()
		newapps=[]
		fault=0
		
		l=len(apps)
		if(not syn==None):
				syn(0,l)
		for i in range(l):
			if(not syn==None):
				syn(i+1,l)
			res=self.updateApp(apps[i])
			if(res.isPositive()):
				newapps.append(res.getData())
			else:
				fault+=1
			
		return Result(ResultEnum.SUCCESS,(l,fault))
	
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
		
		self.logger.warning("deleteAppByAppId()删除app："+appid)
		
		return Result(ResultEnum.SUCCESS)
	
	def deleteAppsByCategory(self,category):
		self.mAppController.deleteAppByCategory(category)
		
		self.logger.warning("deleteAppByCategory()删除分类为'"+category+"'的app")
		
		return Result(ResultEnum.SUCCESS)
	
	def deleteAllApps(self):
		self.mAppController.deleteAllApps()
		self.logger.warning("删除所有app!")
		return Result(ResultEnum.SUCCESS)
				
	def getCategories(self):
		res=self.mAppController.selectCategories()

		if(res==None):
			self.logger.error("getCategories()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
				
		return Result(ResultEnum.SUCCESS,res)
	
	def getPricesByApp(self,app):
		return self.mPriceService.getPricesByAppId(app.getAppId())
	
	def countApp(self):
		res=self.mAppController.countApp()
		
		return Result(ResultEnum.SUCCESS,res)
	
	def countStar(self):
		res=self.mAppController.countStar()
		
		return Result(ResultEnum.SUCCESS,res)
		
	def countCategory(self):
		res=self.mAppController.countCategory()
		
		return Result(ResultEnum.SUCCESS,res)
	
	def countPrices(self):
		res=self.mPriceService.countPrices()
		
		return Result(ResultEnum.SUCCESS,res.getData())
		
	def sumNewestPrices(self):
		res=self.mPriceService.sumNewestPrices()
		
		return Result(ResultEnum.SUCCESS,res.getData())
	
	def starApp(self,app):
		cnt=self.sortAppStar().getData()
		app.setStar(cnt+1)
		self.mAppController.updateApp(app)
		self.logger.info("收藏app："+app.getAppId())

		return Result(ResultEnum.SUCCESS)
	
	def unstarApp(self,app):
		app.setStar(0)
		self.mAppController.updateApp(app)
		self.logger.info("取消收藏app："+app.getAppId())
		
		self.sortAppStar()
		
		return Result(ResultEnum.SUCCESS)	
	
	def changeAppStar(self,app,star):
		if(star<1):
			return self.unstarApp()
		
		app.setStar(star)
		self.mAppController.updateApp(app)
		
		self.logger.info("修改收藏app顺序："+app.getAppId()+" "+str(star))
		return Result(ResultEnum.SUCCESS)
		
	def sortAppStar(self):
		res=self.getAppsByStar()
		if(not res.isPositive()):
			return res

		apps=res.getData()
		cnt=len(apps)

		for i in range(cnt):
			self.changeAppStar(apps[i],i+1)
		
		#self.logger.info("排序app收藏顺序。")
		return Result(ResultEnum.SUCCESS,cnt)	
	
	def changeAppCategory(self,app,category):
		self.logger.info("修改app分类: "+str(app.getId())+" "+app.getApplicationCategory()+" -> "+category)
		app.setApplicationCategory(category)
		res=self.mAppController.updateApp(app)
	
		return Result(ResultEnum.SUCCESS)
	
	def changeAppAutoUpdate(self,app,arg):
		self.logger.info("修改app自动更新: "+str(app.getAppId())+" "+str(arg))
		app.setAutoUpdate(arg)
		res=self.mAppController.updateApp(app)
	
		return Result(ResultEnum.SUCCESS)
	
	def noticePrice(self,app):
		
		res=self.getPricesByApp(app)
		if(not res.isPositive()):
			return res
			
		prices=res.getData()
		
		if (len(prices)<2):
			return Result(ResultEnum.FAULT)
			
		newprice=prices[-1]
		oldprice=prices[-2]
		
		if(newprice.getPrice()>=oldprice.getPrice() or newprice.getNoticed()==1):
			return Result(ResultEnum.FAULT)
		
		self.mPriceService.setNoticed(newprice)
		note='你关注的"'+app.getName()+'"降价啦！🎉 当前价格:¥ '+str(newprice.getPrice())
		self.mNotification.addNotice(note)
		
		self.logger.info("降价通知："+app.getName()+"\n"+newprice.toString())
		return Result(ResultEnum.SUCCESS)
		
	def isExist(self,app):
		if(self.mAppController.selectAppByAppId(app.getAppId()) != None):
			return True
		else:
			return  False

	def clearDataBase(self):
		self.logger.warning("清理数据库:")
		self.deleteAllApps()
		self.mPriceService.deleteAllPrices()	
		return Result(ResultEnum.SUCCESS)

	def setLogger_Run(self,arg):
		self.logger.setRun(arg)
		self.mPriceService.setLogger_Run(arg)
		self.mConfigService.setLogger_Run(arg)
		return Result(ResultEnum.SUCCESS)

if __name__ == "__main__":
	serv=AppService()

	#res=serv.getAppsByStar()

	#if(res.equal(ResultEnum.SUCCESS)):
		#for i in res.getData():
			#print(i.toString()+"\n")
	
