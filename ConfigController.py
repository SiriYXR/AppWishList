# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ConfigController.py
@time: 2020.1.30 13:24
"""

from ConfigModel import Config

from tools.sql.SQLConnector import SQLConnector

class ConfigController (object):
	
	mSQLConn = None
	
	def __init__(self,dbpath):
		self.mSQLConn = SQLConnector(dbpath)
	
	def __del__(self):
		pass
		
	def updateConfig(self,config):
		self.mSQLConn.connect()
		
		sql='''UPDATE config SET runtimes={runtimes},notice={notice},downloadimg={downloadimg},log={log} WHERE id={id}'''.format(runtimes=config.getRunTimes(),notice=config.getNotice(),downloadimg=config.getDownLoadImg(),log=config.getLog(),id=config.getId())
		#print(sql)
		self.mSQLConn.execute(sql)
		
		self.mSQLConn.close()
	
	def selectConfigById(self,id):
		self.mSQLConn.connect()
		
		sql='''SELECT * FROM config WHERE id={id}'''.format(id=id)
		#print(sql)
		self.mSQLConn.execute(sql)
		
		res=self.mSQLConn.fetchone()
		
		self.mSQLConn.close()
		
		config=Config()
		config.initByTuple(res)
		
		return config
		
if __name__ == "__main__":
	cont=ConfigController("data/database.db")
	
	res=cont.selectConfigById(1)
	
	print(res.toString())
	
	res.setNotice(1)
	res.setRunTimes(0)
	res.setDownLoadImg(1)
	
	cont.updateConfig(res)
	
	res=cont.selectConfigById(1)
	
	print(res.toString())
