# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: CheckInternet.py
@time: 2020.1.28 16:58
"""

import requests

def isConnected(url):
	try:
		data=requests.get(url,timeout=2)
	except:
		return False
		
	return True
	
if __name__ == "__main__":
	print(isConnected("https://blog.siriyang.cn"))
