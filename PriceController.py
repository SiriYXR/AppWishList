# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: PriceController.py
@time: 2020.1.28 13:07
"""
from PriceModel import Price
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
		
		sql='''UPDATE price SET appid="{appid}",price={price} WHERE id={id}'''.format(appid=price.getAppId(),price=price.getPrice(),id=price.getId())
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
		
		sql='''SELECT * FROM price ORDER BY creattime'''
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
		
		return res
	
	def selectAllPriceByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE appid="{appid}" ORDER BY creattime'''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		return res
		
	def selectPriceByAppId_Day(self,appid,time):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM price WHERE appid="{appid}" AND strftime("%Y-%m-%d",creattime) = strftime("%Y-%m-%d","{time}") '''.format(appid=appid,time=time)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		return res
	
if __name__ == "__main__":
	cont=PriceController("data/database.db")
	
	
	
