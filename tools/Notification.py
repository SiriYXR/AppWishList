# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: Notification.py
@createTime: 2020.2.1 20:11
@updateTime: 2020-04-05 21:34:34
@codeLines: 13
"""

import notification
import sys

class Notification (object):
	
	def __init__(self,title):
		self.title=title
		rootpath=sys.argv[0]
		localpath=rootpath.split('Documents/')[1]
		self.url='pythonista3://'+localpath+'?action=run'
		
	def addNotice(self,info):
		notification.schedule(message=info,delay=0,sound_name='default',action_url=self.url,title=self.title)
		
if __name__ == "__main__":
	n=Notification("AppWishList")
	n.addNotice('你关注的"Pythonista"降价啦！🎉 当前价格:¥ 0.0')
