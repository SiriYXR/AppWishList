# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: PriceLabel.py
@time: 2020.1.31 12:29
"""

import sys
import ui

sys.path.append("..")

from PriceModel import Price


class PriceLabel (ui.View):
	
	def __init__(self,title,price,title_w,time_h):
		self.frame=(0,0,100,50)
		self.title=title
		self.price=price
		self.title_w=title_w
		self.time_h=time_h
		
		self.titleLabel=ui.Label()
		self.priceLabel=ui.Label()
		self.timeLabel=ui.Label()
		
		self.add_subview(self.titleLabel)
		self.add_subview(self.priceLabel)
		self.add_subview(self.timeLabel)
		
	def layout(self):
		self.timeLabel.frame=(0,self.height-self.time_h,self.width,self.time_h)
		self.titleLabel.frame=(0,0,self.title_w,self.height-self.time_h)
		self.priceLabel.frame=(self.title_w,0,self.width-self.title_w,self.height-self.time_h)
		
		self.titleLabel.font=('Arial',20)
		self.titleLabel.alignment=ui.ALIGN_CENTER
		self.titleLabel.background_color="#638e32"
		self.titleLabel.text_color="white"
		self.titleLabel.text=self.title
		
		priceStr=lambda x : "NULL" if x==-1 else  "¥ "+str(x) if x>0 else "Free"
		self.priceLabel.font=('Arial',20)
		self.priceLabel.alignment=ui.ALIGN_CENTER
		self.priceLabel.background_color="#103142"
		self.priceLabel.text_color="#b7e6fc"
		self.priceLabel.text=priceStr(self.price.getPrice())
		
		timeStr=lambda x ,y: "" if x==-1 else  y 
		self.timeLabel.font=('Arial',10)
		self.timeLabel.background_color="black"
		self.timeLabel.text_color="white"
		self.timeLabel.alignment=ui.ALIGN_CENTER
		self.timeLabel.text=timeStr(self.price.getPrice(),self.price.getUpdateTime())
	
	def updateData(self,price):
		self.price=price
		
		self.layout()
	
if __name__ == "__main__" :
	l=PriceLabel("收藏价格:",Price("",-1),100,15)
	l.frame=(0,0,200,45)
	l.present("sheet")
