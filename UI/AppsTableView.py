# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppsTableView.py
@time: 2020.1.29 00:29
"""

import sys

import ui
import console

from AppDetailView import AppDetailView
from SteamPriceLabel import SteamPriceLabel

sys.path.append("..")

from AppModel import App
from AppService import AppService
from PriceModel import Price
from PriceService import PriceService

from tools.Result import *

class AppsTableView(ui.View):
	def __init__(self,app,father,name):
		self.app=app
		self.father=father
		
		self.name=name
		self.background_color="white"
		self.frame=(0,0,self.app.width,self.app.height)
		self.flex="WHLRTB"
			
		self.tableView = ui.TableView(frame=(0, 0, self.width, self.height))
		self.tableView.flex="WHLRTB"
		self.add_subview(self.tableView)
		
		self.apps=[]
		
		self.tableView.data_source = self
		self.tableView.delegate = self
		
		self.loadData()
		self.loadUI()	
	
	def loadData(self):
		try:
			res=self.app.appService.getAppsByCategory(self.name)
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
			
			self.apps=res.getData() 
			
			self.tableView.reload()
		except Exception as e:
			console.hud_alert('Failed to load Apps', 'error', 1.0)
		finally:
			pass
	
	def loadUI(self):
		self.tableView.frame=self.frame
			
	
	def layout(self):
		self.tableView.reload()
		pass
	
	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.apps)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		app = self.apps[row]
		cell.text_label.text = app.getName()
		cell.detail_text_label.text = app.getAuthor()
		cell.image_view.image=ui.Image.named(self.app.rootpath+"img/"+app.getAppId()+".png")
		cell.accessory_type='disclosure_indicator'
	
		self.loadCellPrice(cell,row)

		return cell
	
	def loadCellPrice(self,cell,row):
		res=self.app.appService.getPricesByApp(self.apps[row])
		
		newprice=0;
		oldprice=0;
		if(not res.equal(ResultEnum.SUCCESS)):
			console.hud_alert(res.toString(), 'error', 1.0)
			newprice=-1;
			oldprice=-1;
		else:
			prices=res.getData()
			if(len(prices)>1):
				newprice=prices[-1].getPrice()
				oldprice=prices[-2].getPrice()
			else:
				newprice=oldprice=prices[0].getPrice()
				
		pricelabel=SteamPriceLabel(oldprice,newprice)
		
		if(self.app.orientation==self.app.LANDSCAPE):
			pricelabel.x,pricelabel.y=self.width-350,10
		else:
			pricelabel.x,pricelabel.y=self.width-220,10
		
		cell.add_subview(pricelabel)
	
	def tableview_can_delete(self, tableview, section, row):
		return True

	def tableview_can_move(self, tableview, section, row):
		return False
	
	@ui.in_background		
	def tableview_did_select(self,tableview, section, row):
		self.app.activity_indicator.start()
		try:
			app = self.apps[row]
			appDetailView = AppDetailView(self.app,self, app)
			self.app.nav_view.push_view(appDetailView)
		except Exception as e:
			console.hud_alert('Failed to load AppDetailView', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	
	def tableview_delete(self,tableview, section, row):
		app=self.apps[row]
			
		res=console.alert("删除应用",'你确定要删除"'+app.getName()+'"吗？',"确定","取消",hide_cancel_button=True)
		
		if(res==1):
			self.deleteApp(app)	
		
	@ui.in_background
	def deleteApp(self,app):
		self.app.activity_indicator.start()
		try:			
			res=self.app.appService.deleteApp(app)
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return
				
			self.loadData()
			self.father.loadData()
		except Exception as e:
			console.hud_alert('Failed to load Apps', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	@ui.in_background		
	def scrollview_did_scroll(self,scrollview):
		if(scrollview.content_offset[1]<-150):
			self.renovate()				
				
	@ui.in_background
	def renovate(self):
		self.app.activity_indicator.start()
		try:
			self.loadData()
			console.hud_alert('刷新成功!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load renovate', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			
