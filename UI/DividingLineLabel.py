# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: DividingLineLabel.py
@time: 2020.1.31 12:06
"""

import ui

class DividingLineLabel(ui.View):
	
	def __init__(self,dw=5,dm=3,dcolor="#d0d0d0"):
		self.dw=dw
		self.dm=dm
		self.dcolor=dcolor
		
		self.frame=(0,0,200,3)
		self.background_color="white"
		
	def layout(self):
		for i in self.subviews:
			self.remove_subview(i)
			
		n=int(self.width/(self.dm+self.dw)+1)
		
		for i in range(n):
			self.add_subview(ui.Label(frame=(i*(self.dm+self.dw),0,self.dw,self.height),bg_color=self.dcolor))

if __name__ == "__main__":
	v=DividingLineLabel()
	v.present("sheet")
		
