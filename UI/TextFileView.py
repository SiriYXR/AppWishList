# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: TextFileView.py
@time: 2020.2.2 14:53
"""
import os

import ui

class TextFileView (ui.View):
	
	def __init__(self,name,path):
		self.path=path
		self.content=""
		self.lines=0
		
		self.name=name
		self.flex="WHRLTB"
		self.background_color="white"
		
		self.scrollView=ui.ScrollView()
		self.contentView=ui.TextView()
		
		self.add_subview(self.contentView)
		#self.add_subview(self.scrollView)
		
		self.loadData()
		
	def loadData(self):
		if(not os.path.exists(self.path)):
			return 
		
		file=open(self.path,mode='r',encoding='utf8')
		datalines=file.readlines()
		self.lines=len(datalines)
		self.content+="当前记录{lines}行日志。\n\n".format(lines=self.lines)
		
		for i in datalines:
			self.content+=i
		
		file.close()		
		
	def loadUI(self):
		self.contentView.text=self.content
		self.contentView.frame=(0,0,self.width,self.height)
		self.contentView.font=("<system>",16)
		
		self.scrollView.frame=(0,0,self.width,self.height)
		self.scrollView.content_size=(self.width,max(self.contentView.height+30,self.height))
		
	def layout(self):
		self.loadUI()
