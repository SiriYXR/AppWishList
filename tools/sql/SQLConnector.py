# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: SQLConnector.py
@time: 2019.12.23 16:28
"""

import sqlite3

class SQLConnector():
	
	path = None 
	conn = None
	cursor = None
	
	def __init__(self,path):
		self.path = path
		
	def connect(self):
		self.conn = sqlite3.connect(self.path)
		self.cursor = self.conn.cursor()
				
	def execute(self,sql):
		return self.cursor.execute(sql)
		
	def fetchone(self):
		return self.cursor.fetchone()
		
	def fetchall(self):
		return self.cursor.fetchall()
		
	def close(self):
		#关闭Cursor:
		self.cursor.close()
		#提交事务：
		self.conn.commit()
		#关闭connection：
		self.conn.close()
		
	
