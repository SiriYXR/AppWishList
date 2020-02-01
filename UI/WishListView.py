# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: WishListView.py
@time: 2020.1.28 21:18
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
from tools.StringProcess import *

class WishListView(ui.View):
	
	def __init__(self,app,father):
		self.app=app
		self.father=father
		
		self.name="愿望单"
		self.background_color="white"
		self.frame=(0,0,self.app.width,self.app.height)
		self.flex="WHLRTB"
		
		self.editBtn=ui.ButtonItem()
		self.editBtn.title="编辑"
		self.editBtn.action=self.edit_Act
		self.right_button_items=[self.editBtn]
					
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
			res=self.app.appService.getAppsByStar()
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
			
			self.apps=res.getData() 
			
		except Exception as e:
			console.hud_alert('Failed to load Apps', 'error', 1.0)
		finally:
			pass
	
	def loadUI(self):
		self.tableView.reload()
		pass		
	
	def layout(self):
		self.loadUI()
		pass
	
	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.apps)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		app = self.apps[row]
		cell.text_label.text = StringProcess(app.getName())
		cell.detail_text_label.text = StringProcess(app.getAuthor())
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
		return True
	
	@ui.in_background		
	def tableview_did_select(self,tableview, section, row):
		self.app.activity_indicator.start()
		try:
			app = self.apps[row]
			appDetailView = AppDetailView(self.app,self, app)
			self.app.nav_view.push_view(appDetailView)
		#except Exception as e:
			#console.hud_alert('Failed to load AppDetailView', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	def tableview_delete(self,tableview, section, row):
		app=self.apps[row]
			
		res=console.alert("移出愿望单",'你确定要将"'+app.getName()+'"移出愿望单吗？',"确定","取消",hide_cancel_button=True)
		
		if(res==1):
			self.unsatrApp(app)	
		
	@ui.in_background
	def unsatrApp(self,app):
		self.app.activity_indicator.start()
		try:			
			res=self.app.appService.unstarApp(app)
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return
				
			self.updateData()
		except Exception as e:
			console.hud_alert('Failed to unsatr Apps', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	@ui.in_background
	def tableview_move_row(self,tableview, from_section, from_row, to_section, to_row):
		self.app.appService.changeAppStar(self.apps[from_row],to_row+1)
		for i in range(to_row,from_row):
			self.app.appService.changeAppStar(self.apps[i],i+2)
		self.loadData()
		
	@ui.in_background		
	def scrollview_did_scroll(self,scrollview):
		if(scrollview.content_offset[1]<-150):
			self.renovate()
				
	@ui.in_background
	def renovate(self):
		self.app.activity_indicator.start()
		try:
			self.updateData()
			console.hud_alert('刷新成功!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load renovate', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
							
	def updateData(self):
		self.loadData()
		self.loadUI()
		self.father.updateData()
	
	def edit_Act(self,sender):
		if(self.tableView.editing):
			self.tableView.editing=False
			self.editBtn.title="编辑"
		else:
			self.tableView.editing=True
			self.editBtn.title="完成"
