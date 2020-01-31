# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppController.py
@time: 2019.12.24 23:01
"""
from AppModel import App

from tools.sql.SQLConnector import SQLConnector

class AppController (object):
	
	mSQLConn = None
	
	def __init__(self,dbpath):
		self.mSQLConn = SQLConnector(dbpath)
	
	def __del__(self):
		pass
		
	def insertApp(self,app):
		self.mSQLConn.connect()
		
		sql='''INSERT INTO apps (appid,url,imgurl,name,applicationCategory,author) VALUES ("{appid}","{url}","{imgurl}", "{name}","{category}","{author}")'''.format(appid=app.getAppId(),url=app.getURL(),imgurl=app.getImgURL(),name=app.getName(),category=app.getApplicationCategory(),author=app.getAuthor())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
		
	def updateApp(self,app):
		self.mSQLConn.connect()
		
		sql='''UPDATE apps SET appid="{appid}",url="{url}",imgurl="{imgurl}",name="{name}",applicationCategory="{category}",author="{author}" WHERE id={id}'''.format(appid=app.getAppId(),url=app.getURL(),imgurl=app.getImgURL(),name=app.getName(),category=app.getApplicationCategory(),author=app.getAuthor(),id=app.getId())
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
		
	def selectAllApps(self):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps '''
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
		
	def selectAppsByCategory(self,category):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM apps WHERE applicationCategory="{category}"'''.format(category=category)
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
		
if __name__ == "__main__":
	cont=AppController("data/database.db")
	
	data=cont.selectAllApps()
	for i in data:
		print(i.toString())
