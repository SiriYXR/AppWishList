# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppDetailView.py
@time: 2020.1.29 20:39
"""

import sys
from datetime import datetime,timedelta

import ui
import console
import webbrowser

from PriceLabel import PriceLabel
from SteamPriceLabel import SteamPriceLabel
from DividingLineLabel import DividingLineLabel
from PricePlotView import PricePlotView

sys.path.append("..")

from AppModel import App
from AppService import AppService
from PriceModel import Price
from PriceService import PriceService

from tools.Result import *
from tools.StringProcess import *

		
class AppDetailView(ui.View):
	
	def __init__(self,app,father,obj):
		self.app=app
		self.father=father
		self.obj=obj
		
		self.presentPrice=Price("",-1)
		self.lastPrice=Price("",-1)
		self.firstPrice=Price("",-1)
		self.lowestPrice=Price("",-1)
		
		self.dates=[]
		self.prices=[]
		self.prices_v=[]
		self.years=[]
		self.epoch=0
		self.loadData()
		
		self.name="应用详情"
		self.background_color="white"
		self.frame=(0,0,self.app.width,self.app.height)
		self.flex="WHLRTB"
		
		self.infoView=ui.View()
		self.info_inconView=ui.ImageView()
		self.info_nameLabel=ui.Label()
		self.info_authorLabel=ui.Label()
		self.info_categoryLabel=ui.Label()
		self.info_createtimeLabel=ui.Label()
		self.info_updatetimeLabel=ui.Label()
		self.info_starBtn=ui.Button()
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
		self.price_offLabel=SteamPriceLabel(self.lastPrice.getPrice(),self.presentPrice.getPrice())
		self.price_normalLabel=PriceLabel("当前价格:",self.presentPrice,100,15)
		self.price_firstLabel=PriceLabel("收藏价格:",self.firstPrice,100,15)
		self.price_lowestLabel=PriceLabel("史低价格:",self.lowestPrice,100,15)
		self.price_TLine_Label=DividingLineLabel(10,5)
		self.price_BLine_Label=DividingLineLabel(10,5)
		
		self.priceView.add_subview(self.price_TLine_Label)
		self.priceView.add_subview(self.price_normalLabel)
		self.priceView.add_subview(self.price_offLabel)
		self.priceView.add_subview(self.price_firstLabel)
		self.priceView.add_subview(self.price_lowestLabel)
		self.priceView.add_subview(self.price_BLine_Label)
		
		self.graphView=ui.View()
		
		self.graph_pricePlot=PricePlotView()
		self.graph_epochBtn=ui.SegmentedControl()
		
		self.graphView.add_subview(self.graph_pricePlot)
		self.graphView.add_subview(self.graph_epochBtn)
		
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
			
			for i in self.prices :
				date=datetime.strptime(i.getCreatTime(),"%Y-%m-%d %H:%M:%S")
				self.dates.append(date)
				self.prices_v.append(i.getPrice())
				
				if(len(self.years)==0 or date.year!=self.years[-1]):
					self.years.append(date.year)
			
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
		self.info_inconView.border_width=4
		self.info_inconView.border_color="#f8f8f8"
		self.info_inconView.corner_radius=30
		
		self.info_nameLabel.text=StringProcess(self.obj.getName())
		
		self.info_authorLabel.text=StringProcess(self.obj.getAuthor())
		self.info_authorLabel.text_color='#979797'
		
		self.info_categoryLabel.text=self.obj.getApplicationCategory()
	
		self.info_createtimeLabel.text="收藏时间:"+self.obj.getCreatTime()
		
		self.info_updatetimeLabel.text="更新时间:"+self.obj.getUpdateTime()
		
		if(self.obj.getStar()>0):
			self.info_starBtn.background_image=ui.Image.named(self.app.rootpath+"UI/img/star_full.PNG")
		else:
			self.info_starBtn.background_image=ui.Image.named(self.app.rootpath+"UI/img/star_vacancy.PNG")
		self.info_starBtn.action=self.star_Act
		
		self.info_storeBtn.title="访问商店"
		self.info_storeBtn.font=('Arial',20)
		#self.info_storeBtn.corner_radius=5
		self.info_storeBtn.bg_color="#2f4658"
		self.info_storeBtn.tint_color="#7ec1ec"
		self.info_storeBtn.action=self.appstore_Act		
		
		self.info_updateBtn.title="更新"
		self.info_updateBtn.font=('Arial',20)
		#self.info_updateBtn.corner_radius=5
		self.info_updateBtn.bg_color="#007800"
		self.info_updateBtn.tint_color="white"
		self.info_updateBtn.action=self.update_Act
		
		self.info_deleteBtn.title="删除"
		self.info_deleteBtn.font=('Arial',20)
		#self.info_deleteBtn.corner_radius=5
		self.info_deleteBtn.bg_color="#cc0000"
		self.info_deleteBtn.tint_color="white"
		self.info_deleteBtn.action=self.delete_Act
		
		'''
		价格信息
		---------------------------------
		'''		
		
		if(self.presentPrice.getPrice()==self.lastPrice.getPrice()):
			self.price_offLabel.hidden=True
		else:
			self.price_offLabel.hidden=False
			
		self.price_offLabel.updateData(self.lastPrice.getPrice(),self.presentPrice.getPrice())
		self.price_normalLabel.updateData(self.presentPrice)
		self.price_firstLabel.updateData(self.firstPrice)
		self.price_lowestLabel.updateData(self.lowestPrice)
			
		'''
		价格图表
		---------------------------------
		'''
		#self.graphView.background_color="red"
		
		self.graph_pricePlot.updateData(self.dates,self.prices_v,self.years[self.epoch])
		
		self.graph_epochBtn.segments=[str(x) for x in self.years]
		self.graph_epochBtn.selected_index=self.epoch
		self.graph_epochBtn.action=self.epoch_Act
		
	
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
		
		margin=(self.width-600)/4
		y=(self.priceView.height-45)/2
		
		if(self.presentPrice.getPrice()==self.lastPrice.getPrice()):
			self.price_normalLabel.frame=(margin,y,200,45)
		else:
			self.price_normalLabel.frame=(margin,(self.priceView.height-55)/2,150,55)
						
		self.price_offLabel.x,self.price_offLabel.y=self.price_normalLabel.x,self.price_normalLabel.y
		
		self.price_firstLabel.frame=(self.price_normalLabel.x+margin+200,y,200,45)
		
		self.price_lowestLabel.frame=(self.price_firstLabel.x+margin+200,y,200,45)
		
		self.price_TLine_Label.frame=(5,0,self.priceView.width-10,2)
		self.price_BLine_Label.frame=(5,self.priceView.height-2,self.priceView.width-10,2)
		
		'''
		价格图表布局
		---------------------------------
		'''	
		self.graphView.frame=(0,self.height*0.4,self.width,self.height*0.6)
		#self.graphView.background_color="red"
				
		self.graph_pricePlot.frame=(0,10,self.width,self.graphView.height)
	
		self.graph_epochBtn.height=25
		self.graph_epochBtn.width=min(50*len(self.years),self.width-40)
		self.graph_epochBtn.x,self.graph_epochBtn.y=max(self.width-max(20+self.graph_epochBtn.width,100),20),10
		
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
		
		margin=(self.width-600)/4
		y=(self.priceView.height-45)/2
		
		if(self.presentPrice.getPrice()==self.lastPrice.getPrice()):
			self.price_normalLabel.frame=(margin,y,200,45)
		else:
			self.price_normalLabel.frame=(margin,(self.priceView.height-55)/2,150,55)
		
		self.price_offLabel.x,self.price_offLabel.y=self.price_normalLabel.x,self.price_normalLabel.y
		
		self.price_firstLabel.frame=(self.price_normalLabel.x+margin+200,y,200,45)
		
		self.price_lowestLabel.frame=(self.price_firstLabel.x+margin+200,y,200,45)
		
		self.price_TLine_Label.frame=(5,0,self.priceView.width-10,2)
		self.price_BLine_Label.frame=(5,self.priceView.height-2,self.priceView.width-10,2)
	
		'''
		价格图表布局
		---------------------------------
		'''	
		self.graphView.frame=(0,self.height*0.4,self.width,self.height*0.6)
		#self.graphView.background_color="red"
				
		self.graph_pricePlot.frame=(0,10,self.width,self.graphView.height)
	
		self.graph_epochBtn.height=25
		self.graph_epochBtn.width=min(50*len(self.years),self.width-40)
		self.graph_epochBtn.x,self.graph_epochBtn.y=max(self.width-max(20+self.graph_epochBtn.width,100),20),10
		
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
			
		
	def star_Act(self,sender):
		if(self.obj.getStar()==0):
			self.starApp()
		else:
			self.unstarApp()	

	def starApp(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.starApp(self.obj)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('App加入愿望单!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to star App', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			pass

	@ui.in_background
	def unstarApp(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.unstarApp(self.obj)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('App已移出愿望单。', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to unstar App', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			pass
			
	def appstore_Act(self,sender):
		webbrowser.open("safari-"+self.obj.getURL())
		
	@ui.in_background
	def update_Act(self,sender):
		self.app.activity_indicator.start()
		try:
			console.hud_alert('开始更新，请等待...', 'success', 1.0)
			res=self.app.appService.updateApp(self.obj)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('更新成功!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to update', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		pass
	
	@ui.in_background
	def renovate_Act(self,sender):
		self.app.activity_indicator.start()
		try:
			self.updateData()
			console.hud_alert('刷新成功!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load renovate', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		pass
	
	def updateData(self):
		self.loadData()
		self.loadUI()
		self.father.updateData()
	
	def delete_Act(self,sender):
		res=console.alert("删除应用",'你确定要删除"'+self.obj.getName()+'"吗？',"确定","取消",hide_cancel_button=True)
		
		if(res==1):
			self.deleteApp()
	
	@ui.in_background	
	def deleteApp(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.deleteApp(self.obj)
			if(not res.isPositive()):
				raise Exception()  
			self.father.updateData()
			console.hud_alert('删除成功!', 'success', 1.0)
			self.app.nav_view.pop_view()
		except Exception as e:
			console.hud_alert('Failed to delete App', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		pass
		
	def epoch_Act(self,sender):
		self.epoch=self.graph_epochBtn.selected_index
		self.loadUI()
		
if __name__ == "__main__":
	pass
