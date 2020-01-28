# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: Result.py
@time: 2019.12.25 12:43
"""

class ResultEnum (object):
	# 基础
	UNKNOW_ERROR = (-1,"Unknow error")
	SUCCESS = (0,"Success")
	FAULT = (1,"Fault")
	
	# 后台
	APP_EXIST=(10,"这个应用已经在愿望单里了！")
	SELECT_ERROR=(11,"查询错误！")
	INVALID_APP=(12,"这不是一个有效的app记录！")
	
	# 网络
	URL_INVALID=(100,"这不是一个有效链接！")
	NET_TIME_OUT=(101,"连接超时！")

class Result (object):
	
	#Result code
	mCode=None
	
	#Result information
	mInfo=None
	
	#Result data
	mData=None
	
	def __init__(self,resultEnum,data=None):
		self.mCode=resultEnum[0]
		self.mInfo=resultEnum[1]
		self.mData=data
		
	def __del__(self):
		pass
		
	def getCode(self):
		return self.mCode
		
	def setCode(self,code):
		self.mCode=code
		
	def getInfo(self):
		return self.mInfo
		
	def setInfo(self,info):
		self.mInfo=info
		
	def getData(self):
		return self.mData
		
	def setData(self,data):
		self.mData=data
		
	def equal(self,enum):
			return self.mCode==enum[0]
	
	def toString(self):
		return "Error Code "+str(self.mCode)+" : "+self.mInfo
		
if __name__ == "__main__":
	res=Result(ResultEnum.SUCCESS)
	
	if(res.equal(ResultEnum.SUCCESS)):
		print(2333)
	
