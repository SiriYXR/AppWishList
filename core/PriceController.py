# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: PriceController.py
@createTime: 2020.1.28 13:07
@updateTime: 2020-03-29 10:54:10
"""

from .PriceModel import Price

from tools.sql.SQLConnector import SQLConnector

class PriceController (object):
	
	mSQLConn = None
	
	def __init__(self,dbpath):
		self.mSQLConn = SQLConnector(dbpath)
	
	def __del__(self):
		pass
		
	def insertPrice(self,price):
		self.mSQLConn.connect()
		
		sql='''INSERT INTO price (appid,price) VALUES ("{appid}","{price}")'''.format(appid=price.getAppId(),price=price.getPrice())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def updatePrice(self,price):
		self.mSQLConn.connect()
		sql='''UPDATE price SET appid="{appid}",price={price},noticed={noticed} WHERE id={id}'''.format(appid=price.getAppId(),price=price.getPrice(),noticed=price.getNoticed(),id=price.getId())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
	
	def deleteAllPrices(self):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM price'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deletePriceById(self,id):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM price WHERE id={id}'''.format(id=id)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deletePriceByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM price WHERE appid="{appid}"'''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def selectAllPrice(self):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price ORDER BY createtime'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		return res
		
		
	def selectPriceById(self,id):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE id={id}'''.format(id=id)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None or len(res)<1):
			return 
		
		price=Price()
		price.initByTuple(res)
		
		return price
	
	def selectPricesByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE appid="{appid}" ORDER BY createtime'''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 
		
		prices=[]
		
		for i in res:
			t=Price()
			t.initByTuple(i)
			prices.append(t)
		
		return prices
		
	def selectPriceByAppId_Day(self,appid,time):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE appid="{appid}" AND strftime("%Y-%m-%d",createtime) = strftime("%Y-%m-%d","{time}") '''.format(appid=appid,time=time)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None or len(res)<1):
			return 
		
		price=Price()
		price.initByTuple(res)
		
		return price
		
	def selectNewestPriceByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE appid="{appid}" AND createtime = (SELECT MAX(createtime) FROM Price WHERE appid="{appid}") '''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None or len(res)<1):
			return 
		
		price=Price()
		price.initByTuple(res)
		
		return price
		
	def countPrices(self):
		self.mSQLConn.connect()
		
		sql='''SELECT COUNT(*) FROM price '''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		return res[0]
		
	def sumNewestPrice(self):
		self.mSQLConn.connect()
		
		sql='''SELECT SUM(price) FROM price WHERE createtime IN (SELECT MAX(createtime) FROM price GROUP BY appid)'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res[0]==None):
			return 0
		
		return res[0]
	
if __name__ == "__main__":
	cont=PriceController("../data/database.db")
	
	print(cont.countPrices())
	print(cont.sumNewestPrice())
