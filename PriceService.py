# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: PriceService.py
@time: 2020.1.28 13:39
"""
import datetime

from AppModel import App
from PriceModel import Price
from PriceController import PriceController

from tools.Result import *
from tools.Logger import *

class PriceService (object):
	
	def __init__(self,rootpath="data/"):
		self.rootpath=rootpath
		
		dbpath=self.rootpath+"database.db"
		self.mPriceController=PriceController(dbpath)
		
		self.logger=Logger(self.rootpath+"log.txt","PriceService.py",True)
		
	def __del__(self):
		pass
		
	def addPrice(self,app,json):
		price=Price(app.getAppId(),json["offers"]["price"])
		
		res=self.mPriceController.selectPriceByAppId_Day(app.getAppId(),datetime.datetime.now().strftime('%Y-%m-%d'))
		
		if(res==None):
			self.mPriceController.insertPrice(price)
			self.logger.info("添加price："+price.toString())
		elif (res[2]>price.getPrice()):
			price.setId(res[0])
			self.mPriceController.updatePrice(price)
			self.logger.info("更新price："+price.toString())
		
		return Result(ResultEnum.SUCCESS,price)
		
	def getPriceByAppId(self,appid):
		res=self.mPriceController.selectPriceByAppId(appid)
		
		prices=[]
		
		for i in res:
			t=Price()
			t.initByTuple(i)
			prices.append[t]
		
		return Result(ResultEnum.SUCCESS,prices)
		
	def deletePriceById(self,id):
		self.mPriceController.deletePriceById(id)
		
		self.logger.warning("删除price: id:"+id)
		return Result(ResultEnum.SUCCESS,id)
		
	def deletePriceByAppId(self,appid):
		self.mPriceController.deletePriceByAppId(appid)
		
		self.logger.warning("删除price: appid:"+appid)
		return Result(ResultEnum.SUCCESS,appid)
