# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: CreatDatabase
@time: 2019.12.24 20:36
"""
import sqlite3
from SQLConnector import SQLConnector

if __name__ == "__main__":
	#创建数据库
	c=SQLConnector("../../data/database.db")
	c.connect()
	
	#打开外键功能
	# c.execute('''PRAGMA foreign_keys=ON''')#sqlite外键功能使用起来不是很方便，还是自己手动实现
	
	#创建表apps
	c.execute('''CREATE TABLE apps(id INTEGER PRIMARY KEY AUTOINCREMENT,appid VARCHAR(255),url VARCHAR(255),imgurl VARCHAR(255),name VARCHAR(255),applicationCategory VARCHAR(255),author VARCHAR(255),creatTime TIMESTAMP DEFAULT(datetime('now','localtime')),updateTime TIMESTAMP DEFAULT(datetime('now','localtime')))''')
	
	#创建触发器，在更新apps表项的时候更新updateTime
	c.execute('''CREATE TRIGGER apps_update BEFORE UPDATE ON apps FOR EACH ROW BEGIN UPDATE apps SET updateTime=datetime('now','localtime') WHERE id= old.id; END;''')
	
	#创建表price
	c.execute('''CREATE TABLE price(id INTEGER PRIMARY KEY AUTOINCREMENT,appid VARCHAR(255),price FLOAT(5),creatTime TIMESTAMP DEFAULT(datetime('now','localtime')),updateTime TIMESTAMP DEFAULT(datetime('now','localtime')))''')
	
	#创建触发器，在更新price表项的时候更新updateTime
	c.execute('''CREATE TRIGGER price_update BEFORE UPDATE ON apps FOR EACH ROW BEGIN UPDATE apps SET updateTime=datetime('now','localtime') WHERE id= old.id; END;''')
	
	c.close()
