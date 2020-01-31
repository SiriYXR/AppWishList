# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ConfigService.py
@time: 2020.1.30 14:00
"""

from ConfigModel import Config
from ConfigController import ConfigController

from tools.Result import *
from tools.Logger import *

class ConfigService (object):
	
	def __init__(self,rootpath="data/"):
		self.rootpath=rootpath
		
		dbpath=self.rootpath+"database.db"
		self.mConfigController=ConfigController(dbpath)
		
		self.logger=Logger(self.rootpath+"log.txt","ConfigService.py",True)
	
	def __del__(self):
		pass

	def init(self):
		res=self.mConfigController.selectConfigById(1)
		
		if(res==None):
			self.logger.error("init()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		res.setRunTimes(0)
		res.setNotice(1)
		res.setDownLoadImg(1)
		
		self.mConfigController.updateConfig(res)
		
		self.logger.info("setNotice success")
		return Result(ResultEnum.SUCCESS,res)
	
	def runTimesAddOne(self):
		res=self.mConfigController.selectConfigById(1)
		
		if(res==None):
			self.logger.error("runTimesAddOne()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		res.setRunTimes(res.getRunTimes()+1)
		
		self.mConfigController.updateConfig(res)
		
		return Result(ResultEnum.SUCCESS,res)	

	def setNotice(self,notice):
		res=self.mConfigController.selectConfigById(1)
		
		if(res==None):
			self.logger.error("setNotice()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		res.setNotice(notice)
		
		self.mConfigController.updateConfig(res)
		
		self.logger.info("setNotice : "+str(notice))
		return Result(ResultEnum.SUCCESS,res)
		
	def setDownLoadImg(self,downloadimg):
		res=self.mConfigController.selectConfigById(1)
		
		if(res==None):
			self.logger.error("setDownLoadImg()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)
		
		res.setDownLoadImg(downloadimg)
		
		self.mConfigController.updateConfig(res)
		
		self.logger.info("setDownLoadImg : "+str(downloadimg))
		return Result(ResultEnum.SUCCESS,res)
	
	def setDefult(self):
		self.logger.info("setDefult:")
		res=self.setNotice(1)
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
		
		res=self.setDownLoadImg(1)
		if(not res.equal(ResultEnum.SUCCESS)):
			return res
			
	def getConfig(self):
		res=self.mConfigController.selectConfigById(1)
		
		if(res==None):
			self.logger.error("getConfig()"+ResultEnum.SELECT_ERROR[1])
			return Result(ResultEnum.SELECT_ERROR)

		return Result(ResultEnum.SUCCESS,res)

	def getRuntimes(self):
		res=self.getConfig()
		
		if(res.isPositive()):
			return Result(ResultEnum.SUCCESS,res.getData().getRunTimes())
		else:
			self.logger.error("getRuntimes()")			
			return res
					
	def getNotice(self):
		res=self.getConfig()
		
		if(res.isPositive()):
			return Result(ResultEnum.SUCCESS,res.getData().getNotice())
		else:
			self.logger.error("getNotice()")
			return res
		
	def getDownLoadImg(self):
		res=self.getConfig()
		
		if(res.isPositive()):
			return Result(ResultEnum.SUCCESS,res.getData().getDownLoad())
		else:
			self.logger.error("getDownLoadImg()")
			return res

if __name__ == "__main__":
	serv=ConfigService()
	
	#serv.runTimesAddOne()
	#serv.setNotice(0)
	#serv.setDownLoadImg(0)
	
	serv.init()
	
	res=serv.getConfig()
	
	if(not res.equal(ResultEnum.SUCCESS)):
		print(res.toString()) 
	else:
		print(res.getData().toString())
		
	
