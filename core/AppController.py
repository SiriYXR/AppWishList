# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: AppController.py
@createTime: 2019.12.24 23:01
@updateTime: 2020-03-29 10:53:38
"""

from .AppModel import App

from tools.sql.SQLConnector import SQLConnector

class AppController (object):
	
	mSQLConn = None
	
	def __init__(self,dbpath):
		self.mSQLConn = SQLConnector(dbpath)
	
	def __del__(self):
		pass
		
	def insertApp(self,app):
		self.mSQLConn.connect()
		
		sql='''INSERT INTO apps (appid,url,imgurl,name,applicationCategory,author,note) VALUES ("{appid}","{url}","{imgurl}", "{name}","{category}","{author}","{note}")'''.format(appid=app.getAppId(),url=app.getURL(),imgurl=app.getImgURL(),name=app.getName(),category=app.getApplicationCategory(),author=app.getAuthor(),note=app.getNote())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def updateApp(self,app):
		self.mSQLConn.connect()

		sql='''UPDATE apps SET appid="{appid}",url="{url}",imgurl="{imgurl}",name="{name}",applicationCategory="{category}",author="{author}",note="{note}",star={star},autoupdate={autoupdate} WHERE id={id}'''.format(appid=app.getAppId(),url=app.getURL(),imgurl=app.getImgURL(),name=app.getName(),category=app.getApplicationCategory(),author=app.getAuthor(),note=app.getNote(),star=app.getStar(),autoupdate=app.getAutoUpdate(),id=app.getId())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deleteAllApps(self):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM apps'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deleteAppById(self,id):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM apps WHERE id={id}'''.format(id=id)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deleteAppByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM apps WHERE appid="{appid}"'''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def deleteAppByCategory(self,category):
		self.mSQLConn.connect()
		
		sql='''DELETE FROM price WHERE appid in (SELECT appid FROM apps WHERE applicationcategory="{category}")'''.format(category=category)
		self.mSQLConn.execute(sql)
			
		sql='''DELETE FROM apps WHERE applicationcategory="{category}"'''.format(category=category)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def selectAllApps(self,where=""):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps {where}'''.format(where=where)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 
		
		apps=[]	
		
		for i in res:
			app=App()
			app.initByTuple(i)
			apps.append(app)
			
		return apps
		
	def selectAppsByCategory(self,category,order=""):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE applicationCategory="{category}" {order}'''.format(category=category,order=order)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 
		
		apps=[]	
		
		for i in res:
			app=App()
			app.initByTuple(i)
			apps.append(app)
			
		return apps
	
	def selectAppsByStar(self):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE star>0 ORDER BY star'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 	
		
		apps=[]	
		
		for i in res:
			app=App()
			app.initByTuple(i)
			apps.append(app)
			
		return apps
	
	def selectAppsByCategoryOrderByNewestPrice(self,category,order=""):
		self.mSQLConn.connect()
	
		sql='''SELECT * FROM (SELECT apps.*,price.price FROM apps,price WHERE apps.appid=price.appid AND price.createtime IN (SELECT MAX(price.createtime) FROM price GROUP BY price.appid)) WHERE applicationcategory="{category}" {order}'''.format(category=category,order=order)
	
		self.mSQLConn.execute(sql)
	
		res=self.mSQLConn.fetchall()
	
		self.mSQLConn.close()
		
		if(res==None):
			return 	
		
		apps=[]	
		
		for i in res:
			app=App()
			app.initByTuple(i)
			apps.append(app)
			
		return apps
	
	def selectAppById(self,id):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE id={id}'''.format(id=id)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 	
		
		app=App()
		app.initByTuple(res)
			
		return app
	
	def selectAppByAppId(self,appid):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE appid="{appid}"'''.format(appid=appid)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 	
		
		app=App()
		app.initByTuple(res)
			
		return app
	
				
	def selectAppByName(self,name):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE name="{name}"'''.format(name=name)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		if(res==None):
			return 	
		
		app=App()
		app.initByTuple(res)
			
		return app
	
	def selectCategories(self):
		self.mSQLConn.connect()
		
		sql='''SELECT applicationCategory FROM apps'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchall()

		self.mSQLConn.close()
		
		if(res==None):
			return 
		
		catdic={}
		
		for i in res:
			if i[0] in catdic:
				catdic[i[0]]+=1
			else:
				catdic[i[0]]=1
		
		return catdic
		
	def countApp(self):
		self.mSQLConn.connect()
		
		sql='''SELECT COUNT(*) FROM apps '''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		return res[0]
		
	def countStar(self):
		self.mSQLConn.connect()
		
		sql='''SELECT COUNT(*) FROM apps WHERE star>0'''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		return res[0]
		
	def countCategory(self):
		self.mSQLConn.connect()
		
		sql='''SELECT COUNT(distinct applicationCategory) FROM apps '''
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		return res[0]
		
if __name__ == "__main__":
	cont=AppController("../data/database.db")
	
	data=cont.selectAllApps()
	for i in data:
		print(i.toString())
		
	print(cont.countCategory())
