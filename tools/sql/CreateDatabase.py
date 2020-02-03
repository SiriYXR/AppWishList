# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: CreateDatabase
@time: 2019.12.24 20:36
"""
import sqlite3
from SQLConnector import SQLConnector

def CreateDataBase(path="../../data/database.db"):
	#创建数据库
	c=SQLConnector(path)
	c.connect()
	
	#打开外键功能
	# c.execute('''PRAGMA foreign_keys=ON''')#sqlite外键功能使用起来不是很方便，还是自己手动实现
	
	#创建表apps
	c.execute('''CREATE TABLE apps(id INTEGER PRIMARY KEY AUTOINCREMENT,appid VARCHAR(255),url VARCHAR(255),imgurl VARCHAR(255),name VARCHAR(255),applicationCategory VARCHAR(255),author VARCHAR(255),note TEXT,star INT(64) DEFAULT(0),autoupdate INT(1) DEFAULT(1),createTime TIMESTAMP DEFAULT(datetime('now','localtime')),updateTime TIMESTAMP DEFAULT(datetime('now','localtime')))''')
	
	#创建触发器，在更新apps表项的时候更新updateTime
	c.execute('''CREATE TRIGGER apps_update BEFORE UPDATE ON apps FOR EACH ROW BEGIN UPDATE apps SET updateTime=datetime('now','localtime') WHERE id= old.id; END;''')
	
	#创建表price
	c.execute('''CREATE TABLE price(id INTEGER PRIMARY KEY AUTOINCREMENT,appid VARCHAR(255),price FLOAT(8) DEFAULT(-1),noticed INT(1) DEFAULT(0),createTime TIMESTAMP DEFAULT(datetime('now','localtime')),updateTime TIMESTAMP DEFAULT(datetime('now','localtime')))''')
	
	#创建触发器，在更新price表项的时候更新updateTime
	c.execute('''CREATE TRIGGER price_update BEFORE UPDATE ON price FOR EACH ROW BEGIN UPDATE price SET updateTime=datetime('now','localtime') WHERE id= old.id; END;''')
	
	#创建表config
	c.execute('''CREATE TABLE config(id INTEGER PRIMARY KEY AUTOINCREMENT,runtimes INT(64) DEFAULT(0),notice INT(1) DEFAULT(0),downloadimg INT(1) DEFAULT(1),log INT(1) DEFAULT(1),createTime TIMESTAMP DEFAULT(datetime('now','localtime')),updateTime TIMESTAMP DEFAULT(datetime('now','localtime')))''')
	
	#创建触发器，在更新config表项的时候更新updateTime
	c.execute('''CREATE TRIGGER config_update BEFORE UPDATE ON config FOR EACH ROW BEGIN UPDATE config SET updateTime=datetime('now','localtime') WHERE id= old.id; END;''')
	
	c.execute('''INSERT INTO config (runtimes,notice,downloadimg,log) VALUES (0,1,1,1) ''')
	
	c.close()


if __name__ == "__main__":
	CreateDataBase()
