# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppModel.py
@time: 2019.12.23 00:25
"""

class App (object):
	
	#记录id
	mId=None
	
	#应用id
	mAppId=None
	
	#应用链接
	mURL=None
	
	#图标链接
	mImgURL=None
	
	#应用名称
	mName=None
	
	#应用类型
	mApplicationCategory=None
	
	#应用作者
	mAuthor=None
	
	#用户备注
	mNote=None
	
	#愿望单top
	mStar=None
	
	#自动更新
	mAutoUpdate=None
	
	#创建时间
	mCreateTime=None
	
	#更新时间	
	mUpdateTime=None
	
	def __init__(self,url=""):
		self.mId=-1
		
		i=url.rfind("id")
		if(i==-1):
			self.mAppId=""
		else:
			self.mAppId=url[i:]
		
		self.mURL=url
		self.mImgURL=""
		self.mName=""
		self.mApplicationCategory=""
		self.mAuthor=""
		self.mNote="暂无备注"
		self.mStar=0
		self.mAutoUpdate=0

	def setId(self,id):
		self.mId=id
		
	def getId(self):
		return self.mId

	def setAppId(self,appid):
		self.mAppId=appid
		
	def getAppId(self):
		return self.mAppId

	def setURL(self,url):
		self.mURL=url
		
	def getURL(self):	
		return self.mURL
		
	def setImgURL(self,url):
		self.mImgURL=url
		
	def getImgURL(self):	
		return self.mImgURL
		
	def setName(self,name):
		self.mName=name
		
	def getName(self):
		return self.mName
		
	def setApplicationCategory(self,category):
		self.mApplicationCategory=category
		
	def getApplicationCategory(self):
		return self.mApplicationCategory
		
	def setAuthor(self,author):
		self.mAuthor=author
		
	def getAuthor(self):
		return self.mAuthor
	
	def setNote(self,note):
		self.mNote=note
		
	def getNote(self):
		return self.mNote
	
	def setStar(self,star):
		self.mStar=star
		
	def getStar(self):
		return self.mStar

	def setAutoUpdate(self,arg):
		self.mAutoUpdate=arg
		
	def getAutoUpdate(self):
		return self.mAutoUpdate

	def getCreateTime(self):
		return self.mCreateTime
		
	def getUpdateTime(self):
		return self.mUpdateTime

	def initByJson(self, json):
		self.mName=json["name"]
		
		self.mImgURL=json["image"]
		
		self.mApplicationCategory=json["applicationCategory"]
		
		self.mAuthor=json["author"]["name"]
	
	def updateByJson(self, json):
		self.mName=json["name"]
		
		self.mImgURL=json["image"]
		
		#self.mApplicationCategory=json["applicationCategory"]
		
		self.mAuthor=json["author"]["name"]
		
	def initByTuple(self,t):
		self.mId=t[0]
		self.mAppId=t[1]
		self.mURL=t[2]
		self.mImgURL=t[3]
		self.mName=t[4]
		self.mApplicationCategory=t[5]
		self.mAuthor=t[6]
		self.mNote=t[7]
		self.mStar=t[8]
		self.mAutoUpdate=t[9]
		self.mCreateTime=t[10]
		self.mUpdateTime=t[11]
		
	def toString(self):
		return 'Id:\t'+str(self.mId)+'\nAppId:\t'+self.mAppId+'\nURL:\t'+self.mURL+'\nName:\t'+self.mName+'\nApplicationCategory:\t'+self.mApplicationCategory+'\nAuthor:\t'+self.mAuthor+'\nNote:\t'+str(self.mNote)+'\nStar:\t'+str(self.mStar)+'\nAutoUpdate:\t'+str(self.mAutoUpdate)
		
if __name__ == "__main__":
	app=App("https://apps.apple.com/cn/app/playdeads-inside/id1201642309")
	app.setId(1)
	#app.setAppId("id123")
	app.setName("test")
	app.setApplicationCategory("game")
	#app.setURL("siriyang.cn")
	app.setAuthor("siriyang")
	
	print(app.toString())
