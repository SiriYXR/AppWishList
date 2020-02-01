# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: StringProcess.py
@time: 2020.1.31 14:09
"""

def StringProcess(str):
	
	str=str.replace("&amp;","&")
	
	return str
	
if __name__ == "__main__" :
	print(StringProcess("1"))
