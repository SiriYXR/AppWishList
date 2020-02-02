# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: PriceModel.py
@time: 2020.1.28 12:50
"""

class Price(object):
	
	#记录id
	mId=None
	
	#应用id
	mAppId=None
	
	#应用价格
	mPrice=None
	
	#是否通知
	mNoticed=None
	
	#创建时间
	mCreateTime=None
	
	#更新时间	
	mUpdateTime=None
	
	def __init__(self,appid="",price=0.0,id=-1):
		self.mId=id
		self.mAppId=appid	
		self.mPrice=price
		self.mNoticed=0
		
	def setId(self,id):
		self.mId=id
		
	def getId(self):
		return self.mId

	def setAppId(self,appid):
		self.mAppId=appid
		
	def getAppId(self):
		return self.mAppId
		
	def setPrice(self,price):
		self.mPrice=price
		
	def getPrice(self):
		return self.mPrice
		
	def setNoticed(self,noticed):
		self.mNoticed=noticed
		
	def getNoticed(self):
		return self.mNoticed
	
	def getCreateTime(self):
		return self.mCreateTime
		
	def getUpdateTime(self):
		return self.mUpdateTime
	
	def initByTuple(self,t):
		self.mId=t[0]
		self.mAppId=t[1]
		self.mPrice=t[2]
		self.mNoticed=t[3]
		self.mCreateTime=t[4]
		self.mUpdateTime=t[5]
	
	def copy(self):
		t=Price()
		t.setId(self.mId)
		t.setAppId(self.mAppId)
		t.setPrice(self.mPrice)
		t.setNoticed(self.mNoticed)
		t.mCreateTime=self.mCreateTime
		t.mUpdateTime=self.mUpdateTime
		
		return t
	
	def toString(self):
		return 'Id: '+str(self.mId)+'\t\tAppId: '+str(self.mAppId)+'\t\tPrice: '+str(self.mPrice)+'\t\tNoticed: '+str(self.mNoticed)
		
if __name__ == "__main__":
	price=Price("1234567890",1.0)
	
	print(price.toString())
	
