# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ConfigModel.py
@time: 2020.1.30 12:18
"""

class Config(object):
	
	#记录id
	mId=None
	
	#程序运行次数
	mRunTimes=None
	
	#是否通知
	mNotice=None
	
	#是否下载图标
	mDownLoadImg=None
	
	#是否记录日志
	mLog=None
	
	#创建时间
	mCreateTime=None
	
	#更新时间	
	mUpdateTime=None
	
	def __init__(self):
		self.mId=-1
		self.mRunTimes=0
		self.mNotice=1
		self.mDownLoadImg=1
		
	def setId(self,id):
		self.mId=id
		
	def getId(self):
		return self.mId

	def setRunTimes(self,runtimes):
		self.mRunTimes=runtimes
		
	def getRunTimes(self):
		return self.mRunTimes

	def setNotice(self,notice):
		self.mNotice=notice
		
	def getNotice(self):
		return self.mNotice	
	
	def setLog(self,log):
		self.mLog=log
		
	def getLog(self):
		return self.mLog
	
	def setDownLoadImg(self,downloadimg):
		self.mDownLoadImg=downloadimg
		
	def getDownLoadImg(self):
		return self.mDownLoadImg
		
	def getCreateTime(self):
		return self.mCreateTime
		
	def getUpdateTime(self):
		return self.mUpdateTime
		
	def initByTuple(self,t):
		self.mId=t[0]
		self.mRunTimes=t[1]
		self.mNotice=t[2]
		self.mDownLoadImg=t[3]
		self.mLog=t[4]
		self.mCreateTime=t[5]
		self.mUpdateTime=t[6]
		
	def toString(self):
		return "Id:"+str(self.mId)+"\tRunTimes:"+str(self.mRunTimes)+"\tNotice:"+str(self.mNotice)+"\tDownLoadImg:"+str(self.mDownLoadImg)+"\tLog:"+str(self.mLog)
