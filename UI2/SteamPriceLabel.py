# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: SteamPriceLabel.py
@CreateTime: 2020.1.30 20:05
@updateTime: 2020-09-01 00:54:47
@codeLines: 81
"""

import ui

class SteamPriceLabel(ui.View):
	
	def __init__(self,old,new,width=150):
		self.old=old
		self.new=new
		
		self.frame=(0,0,width,width/150*40)
		#self.background_color="#103142"
		
		self.off_label=ui.Label()
		self.oldprice_label=ui.Label()
		self.newprice_label=ui.Label()
		self.line=ui.Label()
		
#		self.add_subview(self.off_label)
#		self.add_subview(self.oldprice_label)
#		self.add_subview(self.newprice_label)
#		self.add_subview(self.line)
		
		self.img=None
		self.drawImg()
		
	def layout(self):
#		self.loadOff()
#		self.loadPrice()
		#self.imgView.frame=(0,0,150,40)
		pass
		
	def draw(self):
		self.img.draw(0,0,self.width,self.width/150*40)
		
	def drawImg(self):
		with ui.ImageContext(150,40) as ctx:
			"""-----------draw rate--------------"""
			rate=0
			if(self.old==0):
				rate=abs(self.new-self.old)*100
			else:
				rate=abs(self.new-self.old)/self.old*100	
			
			if(self.old==self.new):
				pass
			elif(self.old<self.new):
				ui.set_color("#eb1a1a")
				ui.fill_rect(0,0,90,40)
				ui.draw_string("+{0:.0f}%".format(rate),(0,7,90,26),('Arial',26),'white',ui.ALIGN_CENTER)
			else:
				ui.set_color("#638e32")
				ui.fill_rect(0,0,90,40)
				ui.draw_string("-{0:.0f}%".format(rate),(0,7,90,26),('Arial',26),"#b6e364",ui.ALIGN_CENTER)
			
			"""-----------draw price--------------"""
			priceStr=lambda x : "NULL" if x==-1 else  "¥ "+str(x) if x>0 else "Free"
							
			if(self.new==self.old):
				ui.set_color("#103142")
				ui.fill_rect(25,0,100,40)
				ui.draw_string(priceStr(self.new),(25,10,100,20),('Arial',20),"#b7e6fc",ui.ALIGN_CENTER)
			else:
				ui.set_color("#103142")
				ui.fill_rect(90,0,60,40)
				ui.draw_string(priceStr(self.new),(90,18,60,18),('Arial',18),"#b7e6fc",ui.ALIGN_CENTER)
				ui.draw_string(priceStr(self.old),(90,4,60,14),('Arial',14),"#b7e6fc",ui.ALIGN_CENTER)
				ui.set_color("#8aa8c7")
				ui.fill_rect(100,12,40,1)
						
			self.img=ctx.get_image()
			
	def loadOff(self):
		self.off_label.frame=(0,0,90,40)
		self.off_label.font=('Arial',26)
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

	def updateData(self,old,new):
		self.old=old
		self.new=new
		
		# self.layout()
		self.drawImg()
		self.set_needs_display()
			
			
if __name__ == "__main__":
	v=SteamPriceLabel(200,100,100)
	
	v.present("sheet")
