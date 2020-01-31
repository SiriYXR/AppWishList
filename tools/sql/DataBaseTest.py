# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: DataBaseTest.py
@time: 2019.12.24 22:57
"""

#导入SQLite驱动：
import sqlite3
from SQLConnector import SQLConnector
	

if __name__ == "__main__":
	c=SQLConnector("../../data/database.db")
	c.connect()
	
	#清空表apps
	c.execute('''DELETE FROM apps''')
	
	#清空表price
	c.execute('''DELETE FROM price''')
	
	c.execute('''insert into apps (appid,url,imgurl,name,applicationCategory,author) values ("123","1","test.png", "Michae","game","siriyang")''')
	
	c.execute('''insert into apps (appid,url,imgurl,name,applicationCategory,author) values ("124","1","test.png", "Michae","game","siriyang")''')
	
	
	res=c.execute('''SELECT * FROM apps''').fetchall()
	for i in res:
		print(i)
	
	c.execute('''insert into price (appid,price,noticed) values("123",1)''')
	
	
	res=c.execute('''SELECT * FROM price''').fetchall()
	for i in res:
		print(i)
	
	c.close()
