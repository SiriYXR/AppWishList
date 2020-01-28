# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ClearDataBase.py
@time: 2019.12.25 09:22
"""

import sqlite3
from SQLConnector import SQLConnector

if __name__ == "__main__":
	#创建数据库
	c=SQLConnector("../../data/database.db")
	c.connect()
	
	#清空表apps
	c.execute('''DELETE FROM apps''')
	
	#清空表price
	c.execute('''DELETE FROM price''')
	
	c.close()
