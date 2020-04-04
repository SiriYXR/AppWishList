# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: DividingLineLabel.py
@time: 2020.1.31 12:06
"""

import ui

class DividingLineLabel(ui.View):
	
	def __init__(self,dw=7,dm=1,dcolor="#d0d0d0"):
		self.dw=dw
		self.dm=dm
		self.dcolor=dcolor
		
		self.frame=(0,0,200,3)
		self.background_color="white"
		
	def draw(self):
		n=int(self.width/(self.dm+self.dw+self.height)+1)
		ui.set_color(self.dcolor)
		for i in range(n):
			for j in range(int(self.height)):
				ui.fill_rect(i*(self.dm+self.dw+self.height)+j,self.height-j,self.dw,1)

if __name__ == "__main__":
	v=DividingLineLabel()
	v.present("sheet")
		
