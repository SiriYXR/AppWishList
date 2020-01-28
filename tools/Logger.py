# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: Logger.py
@time: 2019.12.26 20:48
"""

import time

class Logger (object):
	
	mPath=None
	mLocation=None
	mShowLocation=None
	mIsRun=None
		
	def __init__(self,path,location,isshow=False,isrun=True):
		self.mPath=path
		self.mLocation=location
		self.mShowLocation=isshow
		self.mIsRun=isrun
		
	def getPath(self):
		return self.mPath
		
	def setPath(self,path):
		self.mPath=path
		
	def getLocation(self):
		return self.mLocation
		
	def setLocation(self,location):
		self.mLocation=location
		
	def getShowLocation(self):
		return self.mShowLocation
		
	def setShowLocation(self,arg):
		self.mShowLocation=arg
	
		
	def debug(self,msg):
		if(not self.mIsRun):
			return 
		
		f=open(self.mPath,"a+",encoding="utf8")
		if(self.mShowLocation):
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"debug ("+self.mLocation+") : "+msg+"\n")
		else:
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"debug : "+msg+"\n")
		f.flush()
		f.close()
		
	def info(self,msg):
		if(not self.mIsRun):
			return
			
		f=open(self.mPath,"a+",encoding="utf8")
		if(self.mShowLocation):
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"info ("+self.mLocation+") : "+msg+"\n")
		else:
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"info : "+msg+"\n")
		f.flush()
		f.close()
		
	def warning(self,msg):
		if(not self.mIsRun):
			return
		
		f=open(self.mPath,"a+",encoding="utf8")
		if(self.mShowLocation):
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"warning ("+self.mLocation+") : "+msg+"\n")
		else:
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"warning : "+msg+"\n")
		f.flush()
		f.close()	
	
	def error(self,msg):
		if(not self.mIsRun):
			return
		
		f=open(self.mPath,"a+",encoding="utf8")
		if(self.mShowLocation):
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"error ("+self.mLocation+") : "+msg+"\n")
		else:
			f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) +"error : "+msg+"\n")
		f.flush()
		f.close()
				
if __name__ == "__main__":
	logger=Logger("test.txt","Logger.py",True)
	logger.debug("debug")
	logger.info("info")
	logger.warning("warning")
	logger.error("error")
