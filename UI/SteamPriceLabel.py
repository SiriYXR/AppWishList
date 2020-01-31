# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: SteamPriceLabel.py
@time: 2020.1.30 20:05
"""

import ui

class SteamPriceLabel(ui.View):
	
	def __init__(self,old,new):
		self.old=old
		self.new=new
		
		self.frame=(0,0,150,40)
		self.background_color="#103142"
		
		self.off_label=ui.Label()
		self.oldprice_label=ui.Label()
		self.newprice_label=ui.Label()
		self.line=ui.Label()
		
		self.loadOff()
		self.loadPrice()
		
		self.add_subview(self.off_label)
		self.add_subview(self.oldprice_label)
		self.add_subview(self.newprice_label)
		self.add_subview(self.line)
		
	def loadOff(self):
		self.off_label.frame=(0,0,90,40)
		self.off_label.font=('Arial',30)
		self.off_label.alignment=ui.ALIGN_CENTER
		
		rate=0
		if(self.old==0):
			rate=abs(self.new-self.old)*100
		else:
			rate=abs(self.new-self.old)/self.old*100			
		
		if(self.old==self.new):
			self.off_label.hidden=True
		elif(self.old<self.new):
			self.off_label.text="+{0:.0f}%".format(rate)
			self.off_label.background_color="#eb1a1a"
			self.off_label.text_color="white"
		else:
			self.off_label.text="-{0:.0f}%".format(rate)
			self.off_label.background_color="#638e32"
			self.off_label.text_color="#b6e364"
		
	def loadPrice(self):
		self.newprice_label.text_color="#b7e6fc"
		self.newprice_label.alignment=ui.ALIGN_CENTER
		self.oldprice_label.text_color="#8aa8c7"
		self.oldprice_label.alignment=ui.ALIGN_CENTER
		self.line.text_color="#8aa8c7"
		self.line.alignment=ui.ALIGN_CENTER

		priceStr=lambda x : "NULL" if x==-1 else  "¥ "+str(x) if x>0 else "Free"
						
		if(self.new==self.old):
			self.background_color="none"
			self.newprice_label.text=priceStr(self.new)
			self.newprice_label.frame=(25,0,100,40)
			self.newprice_label.background_color="#103142"
			self.newprice_label.font=('Arial',20)
		else:
			self.newprice_label.text=priceStr(self.new)
			self.oldprice_label.text=priceStr(self.old)
			
			self.newprice_label.frame=(90,16,60,25)
			self.newprice_label.font=('Arial',18)
			
			self.oldprice_label.frame=(90,0,60,25)
			self.oldprice_label.font=('Arial',14)
			
			self.line.frame=(90,-1,60,25)
			self.line.text="——"

			
			
if __name__ == "__main__":
	v=SteamPriceLabel(200,200)
	
	v.present("sheet")
