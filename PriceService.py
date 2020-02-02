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
			return Result(ResultEnum.SUCCESS,price)
		else:
			res.setPrice(price.getPrice())
			self.mPriceController.updatePrice(res)
			self.logger.info("更新price："+res.toString())
			return Result(ResultEnum.PRICE_UPDATE,res)
		
		return Result(ResultEnum.SUCCESS,res)
		
	def getPricesByAppId(self,appid):
		res=self.mPriceController.selectPricesByAppId(appid)
		
		if(res==None):
			self.logger.error("getPricesByAppId()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
						
		return Result(ResultEnum.SUCCESS,res)
		
	def setNoticed(self,price):
		price.setNoticed(1)
		self.mPriceController.updatePrice(price)
		self.logger.info("通知price："+price.toString())
		
		return Result(ResultEnum.PRICE_NOTICED,price)
		
	def deletePriceById(self,id):
		self.mPriceController.deletePriceById(id)
		
		self.logger.warning("删除price: id:"+id)
		return Result(ResultEnum.SUCCESS,id)
		
	def deletePriceByAppId(self,appid):
		self.mPriceController.deletePriceByAppId(appid)
		
		self.logger.warning("删除price: appid:"+appid)
		return Result(ResultEnum.SUCCESS,appid)
		
	def deleteAllPrices(self):
		self.mPriceController.deleteAllPrices()
		self.logger.warning("删除所有price!")
		return Result(ResultEnum.SUCCESS)
		
	def countPrices(self):
		res=self.mPriceController.countPrices()
		
		return Result(ResultEnum.SUCCESS,res)

	def sumNewestPrices(self):
		res=self.mPriceController.sumNewestPrice()
		
		return Result(ResultEnum.SUCCESS,res)
		
	def setLogger_Run(self,arg):
		self.logger.setRun(arg)
			
if __name__ == "__main__":
	pass
