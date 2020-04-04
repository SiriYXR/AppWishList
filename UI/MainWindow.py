# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: MainWindow.py
@createTime: 2020-01-28 18:59
@updateTime: 2020-04-03 23:38:46
@codeLines: 175
"""

import ui
import console
import webbrowser

from .WishListView import WishListView
from .CategoryView import CategoryView
from .SettingView import SettingView
from .UpdateDataView import UpdateDataView

from core.AppModel import App
from core.AppService import AppService
from core.ConfigService import ConfigService

from tools.Result import *

class MainTable(ui.View):
	
	MENU_WISHLIST="愿望单"
	MENU_FAVORITE="收藏夹"
	MENU_UPDATE="更新数据"
	MENU_SETTING="设置"
	MENU_ABOUT="关于"
	MENU_COPYRIGHT="Copyright © 2020 by SiriYang. v1.1.2"
	MENU_BLOG="blog.siriyang.cn"
	
	def __init__(self, app):
		self.app = app
		self.menuList=[]
				
		self.name = '首页'
		self.background_color="white"
		self.flex='WHLRTB'
		
		self.tableView=ui.TableView()
		self.tableView.flex='HLRTB'
		if self.app.isIpad():
			self.tableView.width=710
		else:
			self.tableView.width=414
		
		self.add_subview(self.tableView)
		
		self.loadData()
		self.loadUI()
		
	def loadData(self):
		self.menuList=[
			"","",
			self.MENU_WISHLIST,
			self.MENU_FAVORITE,
			"",
			self.MENU_UPDATE,
			self.MENU_SETTING,
			"",
			self.MENU_ABOUT,
			"","","",
			self.MENU_COPYRIGHT,
			self.MENU_BLOG,
			]
	
	def loadUI(self):
		self.tableView.data_source = self
		self.tableView.delegate = self
		self.tableView.reload()
	
	def tableview_number_of_rows(self,tableview,section):
		return len(self.menuList)
	
	def tableview_cell_for_row(self,tableview,section,row):
		cell=ui.TableViewCell()
		cell.selectable=False
		
		opt_name = self.menuList[row]
		label=ui.Label()
		label.alignment=ui.ALIGN_CENTER
		label.frame=(0,0,tableview.width,cell.height)
		label.text=opt_name
		if (opt_name==self.MENU_WISHLIST):
			cell.image_view.image=ui.Image.named('typb:Star')
			cell.accessory_type='disclosure_indicator'
		elif (opt_name==self.MENU_FAVORITE):
			cell.image_view.image=ui.Image.named('typb:List')
			cell.accessory_type='disclosure_indicator'
		elif (opt_name==self.MENU_UPDATE):
			cell.image_view.image=ui.Image.named('typb:Refresh')
		elif (opt_name==self.MENU_SETTING):
			cell.image_view.image=ui.Image.named('typb:Cog')
			cell.accessory_type='disclosure_indicator'
		elif (opt_name==self.MENU_ABOUT):
			cell.image_view.image=ui.Image.named('typb:Info')
			
		cell.content_view.add_subview(label)
		return cell
	
	def tableview_did_select(self,tableview,section,row):
		opt_name = self.menuList[row]
		if (opt_name==self.MENU_WISHLIST):
			self.WishList_act()
		elif (opt_name==self.MENU_FAVORITE):
			self.Favorite_act()
		elif (opt_name==self.MENU_UPDATE):
			if(self.app.isUpdating):
				console.hud_alert('数据更新中，请稍等！', 'error', 1.0)
				return
				
			console.hud_alert('开始更新中，请稍等！', 'success', 1.0) 
			self.app.isUpdating=True
			self.Update_act()
		elif (opt_name==self.MENU_SETTING):
			self.Setting_act()
		elif (opt_name==self.MENU_ABOUT):
			self.About_act()
		elif (opt_name==self.MENU_BLOG):
			self.Blog_act()
		
	def WishList_act(self):
		v = WishListView(self.app,self)
		self.app.nav_view.push_view(v)

	def Favorite_act(self):
		v = CategoryView(self.app,self)
		self.app.nav_view.push_view(v)

	@ui.in_background
	def Update_act(self):
		try:
			UpdateDataView(self.app)	
		except Exception as e:
			console.hud_alert('Failed to update', 'error', 1.0)
		finally:
			self.app.isUpdating=False
	
	def updateData(self):
		self.loadData()
	
	def Setting_act(self):
		v = SettingView(self.app,self)
		if self.app.isIpad():
			v.frame=(0,0,550,600)
			v.present("sheet")
		else:
			v.frame=(0,0,self.width,self.height)
			self.app.nav_view.push_view(v)
			
	def About_act(self):
		webbrowser.open("safari-https://blog.siriyang.cn/posts/20200202171851id.html")
	
	def Blog_act(self):
		webbrowser.open("safari-https://blog.siriyang.cn")

class MainWindow(ui.View):
	
	LANDSCAPE=0
	PORTRAIT=1
	
	IPAD=0
	IPHONE=1
	
	NORMAL=0
	TEST_IPHOE_L=1
	TEST_IPHOE_P=2
	
	def __init__(self,rootpath,test_mod=0):
		self.name = 'AppWishList'
		self.rootpath=rootpath
		self.appService=AppService(rootpath)
		self.configService=ConfigService(rootpath)
		
		self.isUpdating=False
		self.orientation = self.LANDSCAPE
		self.divice=self.IPAD
		self.test_mod=test_mod
								
		self.activity_indicator = ui.ActivityIndicator(flex='LTRB')
		self.activity_indicator.style = 10
		
		if self.test_mod==self.NORMAL:
			self.width,self.height=ui.get_window_size()
		elif self.test_mod==self.TEST_IPHOE_P:
			# iPhone test
			self.width,self.height=414,736
		else:
			self.width,self.height=736,414
		if(self.width+self.height<1024+768):
			self.divice=self.IPHONE
		
		self.mainTable=MainTable(self)
		self.nav_view=ui.NavigationView(self.mainTable)
		self.nav_view.flex="WHLRTB"
		
		self.nav_view.add_subview(self.activity_indicator)
		self.add_subview(self.nav_view)

		self.loadUI()
		
		self.activity_indicator.bring_to_front()
		
	def loadUI(self):
		self.nav_view.frame=(0,0,self.width,self.height)
		self.activity_indicator.frame = (0, 0, self.nav_view.width, self.nav_view.height)
		
	def layout(self):
		if self.width > self.height:
			self.orientation=self.LANDSCAPE
		else:
			self.orientation=self.PORTRAIT
	
	def launch(self):
		if self.test_mod==self.NORMAL:
			self.present(style='fullscreen')
		else:
			self.present(style='sheet')
		self.configService.runTimesAddOne()

	def isIpad(self):
		return self.divice==self.IPAD

if __name__ == '__main__':
	mainWindow = MainWindow("../data/")
	mainWindow.launch()
