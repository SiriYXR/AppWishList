# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: PricePlotView.py
@time: 2020.1.31 15:09
"""

from datetime import datetime,timedelta
import random

import ui

class AxeLabel(ui.View):
	def __init__(self,text,t,tc="black",lc="black",frame=(0,0,100,20)):		
		self.t=t
		self.frame=frame
		
		self.line=ui.Label()
		self.line.background_color=lc
		self.lw=5
		self.lh=2
		
		self.info=ui.Label()
		self.info.text=text
		self.info.alignment=ui.ALIGN_RIGHT
		self.info.text_color=tc
		
		self.add_subview(self.line)
		self.add_subview(self.info)
		
	def layout(self):
		if(self.t==0):
			self.line.frame=(self.width-self.lw,(self.height-self.lh)/2,self.lw,self.lh)
			self.info.frame=(0,0,self.width-self.lw,self.height)
		else:
			self.line.frame=((self.width-self.lh)/2,0,self.lh,self.lw)
			self.info.frame=(0,self.lw,self.width-self.lw,self.height)
			
		
class PriceBar(ui.View):
	def __init__(self,father,index,color="#6cc5f1"):
		self.father=father
		self.index=index
		self.color=color
		
	def layout(self):
		self.background_color=self.color
	
	def touch_began(self,touch):
		self.father.showInfo(self.index)
	
	def touch_ended(self,touch):
		self.father.hideInfo()
	
class PricePlotView(ui.View):
	
	COLOR_EVEN="#6cc5f1"
	COLOR_UP="#cc0000"
	COLOR_DOWN="#729c0b"
	COLOR_NONE="#a7a7a7"
	
	def __init__(self):
		self.data_x=[]
		self.data_y=[]
		self.org_y=[]
		self.epoch=-1
		self.index=-1
		
		self.offset_x=100
		self.offsey_y=50
		
		self.scrollView=ui.ScrollView()
		self.scrollView.delegate=self
		
		self.scrollViewitems=[]
		
		self.x_axe=ui.Label()
		self.x_axe.background_color="#494949"
		self.y_axe=ui.Label()
		self.y_axe.background_color="#494949"
		
		self.scrollView.add_subview(self.x_axe)
		self.scrollView.add_subview(self.y_axe)
		
		self.info_label=ui.Label()
		self.info_label.frame=(0,0,220,20)
		self.info_label.background_color="#103142"
		self.info_label.text_color="#b7e6fc"
		self.info_label.alignment=ui.ALIGN_CENTER
		self.info_label.hidden=True
		
		self.add_subview(self.scrollView)
		self.add_subview(self.info_label)
		
	def loadData(self,x,y):
		if(len(x)==0):
			return 
		
		self.org_y=y
		self.index=0
		while x[self.index].strftime("%Y%m%d")< "{Y}0101".format(Y=self.epoch):
			self.index+=1
			
		date=x[self.index]
		i=self.index	
		while date.strftime("%Y%m%d") <= x[-1].strftime("%Y%m%d") and date.strftime("%Y%m%d") < "{Y}0101".format(Y=self.epoch+1):
			self.data_x.append(date)
			date+=timedelta(days=1)
			if((x[i]-date).days<1):
				self.data_y.append(y[i])
				i+=1
			else:
				self.data_y.append(-1)
		
	def layout(self):
		for i in self.scrollViewitems:
			self.remove_subview(i)
		
		getWidth = lambda x : len(self.data_x)*20+self.offset_x*2 if len(self.data_x)*20+self.offset_x*2>self.width else self.width
		self.scrollView.frame=(0,0,self.width,self.height)
		self.scrollView.content_size=(getWidth(self.data_x),self.height)
		self.scrollView.scroll_enabled=True
		self.scrollView.always_bounce_horizontal=True
		self.scrollView.background_color="white"
		
		self.x_axe.frame=(self.offset_x-10,self.height-self.offsey_y,getWidth(self.data_x)-2*self.offset_x+20,5)
		
		self.y_axe.frame=(self.offset_x-10,40,5,self.height-self.offsey_y-40)
		
		for i in range(int((self.y_axe.height-25)/25)):
			if(i==0):
				t=AxeLabel("free",0,"#494949","#494949",(50,self.height-self.offsey_y-60,40,20))
				self.scrollViewitems.append(t)
				self.scrollView.add_subview(t)
				t=ui.Label(frame=(self.x_axe.x+5,self.height-self.offsey_y-50,self.x_axe.width,2),background_color="#f1f1f1")
				self.scrollViewitems.append(t)
				self.scrollView.add_subview(t)
			else:
				t=AxeLabel(str(i*25),0,"#494949","#494949",(50,self.height-self.offsey_y-60-i*25,40,20))
				self.scrollViewitems.append(t)
				self.scrollView.add_subview(t)
				t=ui.Label(frame=(self.x_axe.x+5,self.height-self.offsey_y-50-i*25,self.x_axe.width,2),background_color="#f1f1f1")
				self.scrollViewitems.append(t)
				self.scrollView.add_subview(t)
						
		data_index=self.index
		for i in range(len(self.data_x)):
			bar=PriceBar(self,i)
			
			if(self.data_y[i]>=0):
				if(data_index>0 and data_index< len(self.org_y) and self.org_y[data_index]>self.org_y[data_index-1]):
					bar.color=self.COLOR_UP
				elif (data_index>0 and data_index< len(self.org_y) and self.org_y[data_index]<self.org_y[data_index-1]):
					bar.color=self.COLOR_DOWN
					
				data_index+=1
										
			bar.frame=(i*20+self.offset_x,self.height-self.data_y[i]-self.offsey_y-50,15,self.data_y[i]+50)
			
			if(self.data_y[i]<0):
				bar.color=self.COLOR_NONE
				bar.height=50
				bar.y=self.height-self.offsey_y-50
			
			if (self.data_x[i].day==1 or self.data_x[i].day==15 or self.data_x[i].strftime("%m%d")=="1230"):
				datestr=str(self.data_x[i].year)+"年"+str(self.data_x[i].month)+"月"+str(self.data_x[i].day)+"日"
				t=AxeLabel(datestr,1,"#494949","#494949",(self.offset_x+i*20-68,self.height-self.offsey_y+4,150,25))
				self.scrollViewitems.append(t)
				self.scrollView.add_subview(t)

			self.scrollViewitems.append(bar)
			self.scrollView.add_subview(bar)
	
	def showInfo(self,i):
		if(self.data_y[i]<0):
			return
		
		self.info_label.hidden=False
		
		x,_=self.scrollView.content_offset
		
		datestr=" ("+str(self.data_x[i].year)+"年"+str(self.data_x[i].month)+"月"+str(self.data_x[i].day)+"日)"
		
		self.info_label.text="¥ "+str(self.data_y[i])+datestr
		self.info_label.x=self.offset_x+i*20-x+10
		self.info_label.y=self.height-self.data_y[i]-self.offsey_y-75
		
		if(self.info_label.x+self.info_label.width>self.width):
			self.info_label.x-=self.info_label.width
		
	def hideInfo(self):
		self.info_label.hidden=True
		
	def scrollview_did_scroll(self,scrollview):
		self.hideInfo()
	
	def updateData(self,x,y,epoch=-1):
		self.data_x=[]
		self.data_y=[]
		self.epoch=epoch
		
		self.loadData(x,y)
		
		self.layout()	

if __name__ == "__main__":
	
	day=[]
	p=[]
	date=datetime.strptime("2020-01-1","%Y-%m-%d")
	while date <= datetime.strptime("2021-01-03","%Y-%m-%d"):
		day.append(date)
		date+=timedelta(days=1)
		p.append(random.randint(30,200)/1.0)
	
	v=PricePlotView()
	v.updateData(day,p,2020)
	v.frame=(0,0,800,400)
	v.present("sheet")
		
