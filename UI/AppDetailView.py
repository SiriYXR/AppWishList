# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppDetailView.py
@time: 2020.1.29 20:39
"""

import sys

import ui
import console
import webbrowser

from SteamPriceLabel import SteamPriceLabel

sys.path.append("..")

from AppModel import App
from AppService import AppService
from PriceModel import Price
from PriceService import PriceService

from tools.Result import *

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
		
class AppDetailView(ui.View):
	
	def __init__(self,app,father,obj):
		self.app=app
		self.father=father
		self.obj=obj
		self.presentPrice=Price("",-1)
		self.lastPrice=Price("",-1)
		self.firstPrice=Price("",-1)
		self.lowestPrice=Price("",-1)
		
		self.name="应用详情"
		self.background_color="white"
		self.frame=(0,0,self.app.width,self.app.height)
		self.flex="WHLRTB"
		
		self.prices=[]
		self.loadData()
		
		self.infoView=ui.View()
		self.info_inconView=ui.ImageView()
		self.info_nameLabel=ui.Label()
		self.info_authorLabel=ui.Label()
		self.info_categoryLabel=ui.Label()
		self.info_createtimeLabel=ui.Label()
		self.info_updatetimeLabel=ui.Label()
		self.info_starBtn=ui.ImageView()
		self.info_storeBtn=ui.Button()
		self.info_updateBtn=ui.Button()
		self.info_deleteBtn=ui.Button()
		
		self.infoView.add_subview(self.info_inconView)
		self.infoView.add_subview(self.info_nameLabel)
		self.infoView.add_subview(self.info_authorLabel)
		self.infoView.add_subview(self.info_categoryLabel)
		self.infoView.add_subview(self.info_createtimeLabel)
		self.infoView.add_subview(self.info_updatetimeLabel)
		self.infoView.add_subview(self.info_starBtn)
		self.infoView.add_subview(self.info_storeBtn)
		self.infoView.add_subview(self.info_updateBtn)
		self.infoView.add_subview(self.info_deleteBtn)
		
		self.priceView=ui.View()
		self.price_presentLabel=SteamPriceLabel(self.presentPrice.getPrice(),self.lastPrice.getPrice())
		self.price_firstLabel=PriceLabel("收藏价格:",self.firstPrice,100,15)
		self.price_lowestLabel=PriceLabel("史低价格:",self.lowestPrice,100,15)
		
		self.priceView.add_subview(self.price_presentLabel)
		self.priceView.add_subview(self.price_firstLabel)
		self.priceView.add_subview(self.price_lowestLabel)
		
		self.graphView=ui.View()
		
		self.add_subview(self.infoView)
		self.add_subview(self.priceView)
		self.add_subview(self.graphView)
		
		self.loadUI()
		
	def loadData(self):
		try:
			res=self.app.appService.getPricesByApp(self.obj)
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
			
			self.prices=res.getData()
			if(len(self.prices)>1):
				self.presentPrice=self.prices[-1]
				self.lastPrice=self.prices[-2]
				self.firstPrice=self.prices[0]
				
				for i in self.prices :
					if(i.getPrice()<self.lowestPrice.getPrice() or self.lowestPrice.getPrice()==-1):
						self.lowestPrice=i
						
			else:
				self.presentPrice=self.lastPrice=self.firstPrice=self.lowestPrice=self.prices[0]
			
		except Exception as e:
			console.hud_alert('Failed to load Prices', 'error', 1.0)
		finally:
			pass
		
	def loadUI(self):
		'''
		基本信息
		---------------------------------
		'''
		self.infoView.background_color="#fff"
		
		self.info_inconView.image=ui.Image.named(self.app.rootpath+"img/"+self.obj.getAppId()+".png")
		
		self.info_nameLabel.text=self.obj.getName()
		
		self.info_authorLabel.text=self.obj.getAuthor()
		self.info_authorLabel.text_color='#979797'
		
		self.info_categoryLabel.text=self.obj.getApplicationCategory()
	
		self.info_createtimeLabel.text="收藏时间:"+self.obj.getCreatTime()
		
		self.info_updatetimeLabel.text="更新时间:"+self.obj.getUpdateTime()
		
		self.info_starBtn.image=ui.Image.named(self.app.rootpath+"UI/img/star_full.PNG")
		
		self.info_storeBtn.title="访问商店"
		self.info_storeBtn.tint_color="white"
		self.info_storeBtn.border_width=2
		self.info_storeBtn.corner_radius=5
		self.info_storeBtn.border_color="#2671ff"
		self.info_storeBtn.bg_color="#2671ff"
		self.info_storeBtn.action=self.appstore		
		
		self.info_updateBtn.title="更新"
		self.info_updateBtn.tint_color="white"
		self.info_updateBtn.border_width=2
		self.info_updateBtn.corner_radius=5
		self.info_updateBtn.border_color="green"
		self.info_updateBtn.bg_color="green"
		
		self.info_deleteBtn.title="删除"
		self.info_deleteBtn.tint_color="white"
		self.info_deleteBtn.border_width=2
		self.info_deleteBtn.corner_radius=5
		self.info_deleteBtn.border_color="red"
		self.info_deleteBtn.bg_color="red"
		
		'''
		价格信息
		---------------------------------
		'''		
		
		
		
		'''
		价格图表
		---------------------------------
		'''
		pass
	
	def layout(self):
		if(self.app.orientation==self.app.LANDSCAPE):
			self.layOut_L()
		else:
			self.layOut_P()
	
	def layOut_L(self):
		'''
		基本信息布局
		---------------------------------
		'''
		self.infoView.frame=(0,0,self.width,self.height*0.3)
		
		self.info_inconView.frame=(20,20,160,160)
		
		self.info_nameLabel.frame=(self.info_inconView.width+40,20,600,40)
		#self.info_nameLabel.background_color="blue"
		
		self.info_authorLabel.frame=(self.info_nameLabel.x,50,600,40)
		#self.info_authorLabel.background_color="blue"
		
		self.info_categoryLabel.frame=(self.info_authorLabel.x,80,120,40)
		#self.info_categoryLabel.background_color="blue"
		
		self.info_createtimeLabel.frame=(self.info_categoryLabel.x,self.info_categoryLabel.y+self.info_categoryLabel.height,260,30)
		#self.info_createtimeLabel.background_color="green"
		
		self.info_updatetimeLabel.frame=(self.info_createtimeLabel.x,self.info_createtimeLabel.y+30,260,30)
		#self.info_updatetimeLabel.background_color="green"
		
		self.info_starBtn.frame=(self.width-100,20,60,60)
		#self.info_starBtn.background_color="orange"
		
		self.info_storeBtn.frame=(self.info_createtimeLabel.x+self.info_createtimeLabel.width+20,120,150,50)
		#self.info_storeBtn.background_color="blue"
		
		self.info_updateBtn.frame=(self.info_storeBtn.x+self.info_storeBtn.width+40,120,150,50)
		#self.info_updateBtn.background_color="blue"
		
		self.info_deleteBtn.frame=(self.info_updateBtn.x+self.info_updateBtn.width+40,120,150,50)
		#self.info_deleteBtn.background_color="red"
	
		'''
		价格信息布局
		---------------------------------
		'''		
		self.priceView.frame=(0,self.height*0.3,self.width,self.height*0.1)
		#self.priceView.background_color="blue"
		
		self.price_presentLabel.x,self.price_presentLabel.y=20,20
		
		self.price_firstLabel.frame=(self.width*0.3,20,200,45)
		
		self.price_lowestLabel.frame=(self.width*0.6,20,200,45)
		
		
		'''
		价格图表布局
		---------------------------------
		'''	
		self.graphView.frame=(0,self.height*0.4,self.width,self.height*0.6)
		#self.graphView.background_color="red"
	
	def layOut_P(self):
		'''
		基本信息布局
		---------------------------------
		'''
		self.infoView.frame=(0,0,self.width,self.height*0.3)
		
		self.info_inconView.frame=(20,20,160,160)
		
		self.info_nameLabel.frame=(self.info_inconView.width+40,20,460,40)
		#self.info_nameLabel.background_color="blue"
		
		self.info_authorLabel.frame=(self.info_nameLabel.x,50,460,40)
		#self.info_authorLabel.background_color="blue"
		
		self.info_categoryLabel.frame=(self.info_authorLabel.x,80,120,40)
		#self.info_categoryLabel.background_color="blue"
		
		self.info_createtimeLabel.frame=(self.info_categoryLabel.x,self.info_categoryLabel.y+self.info_categoryLabel.height,260,30)
		#self.info_createtimeLabel.background_color="green"
		
		self.info_updatetimeLabel.frame=(self.info_createtimeLabel.x,self.info_createtimeLabel.y+30,260,30)
		#self.info_updatetimeLabel.background_color="green"
		
		self.info_starBtn.frame=(self.width-80,20,60,60)
		#self.info_starBtn.background_color="orange"
		
		self.info_storeBtn.frame=(self.info_updatetimeLabel.x,self.info_updatetimeLabel.y+self.info_updatetimeLabel.height+20,150,50)
		#self.info_storeBtn.background_color="blue"
		
		self.info_updateBtn.frame=(self.info_storeBtn.x+self.info_storeBtn.width+40,self.info_updatetimeLabel.y+self.info_updatetimeLabel.height+20,150,50)
		#self.info_updateBtn.background_color="blue"
		
		self.info_deleteBtn.frame=(self.info_updateBtn.x+self.info_updateBtn.width+40,self.info_updatetimeLabel.y+self.info_updatetimeLabel.height+20,150,50)
		#self.info_deleteBtn.background_color="red"
		
		'''
		价格信息布局
		---------------------------------
		'''		
		self.priceView.frame=(0,self.height*0.3,self.width,self.height*0.1)
		#self.priceView.background_color="blue"
		
		self.price_presentLabel.x,self.price_presentLabel.y=20,20
		
		self.price_firstLabel.frame=(self.width*0.3,20,200,45)
		
		self.price_lowestLabel.frame=(self.width*0.6,20,200,45)
		
		pass
	
	@ui.in_background
	def load(self):
		self.app.activity_indicator.start()
		try:
			self.loadData()
			self.loadUI()
			
		except Exception as e:
			console.hud_alert('Failed to load Prices', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			
	def appstore(self,sender):
		webbrowser.open("safari-"+self.obj.getURL())
		
if __name__ == "__main__" :
	l=PriceLabel("收藏价格:",Price("",-1),100,15)
	l.frame=(0,0,200,45)
	l.present("sheet")
