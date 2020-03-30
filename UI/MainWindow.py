# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: MainWindow.py
@createTime: 2020-01-28 18:59
@updateTime: 2020-03-30 09:25:02
@codeLines: 197
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
	
	IPAD_MENU_WISHLIST="\t\t\t\t\t\t\t\t\t愿望单"
	IPAD_MENU_FAVORITE="\t\t\t\t\t\t\t\t\t收藏夹"
	IPAD_MENU_UPDATE="\t\t\t\t\t\t\t\t    更新数据"
	IPAD_MENU_SETTING="\t\t\t\t\t\t\t\t\t  设置"
	IPAD_MENU_ABOUT="\t\t\t\t\t\t\t\t\t  关于"
	IPAD_MENU_COPYRIGHT="\t\t\t\t\t\t\tCopyright © 2020 by SiriYang. v1.1.1"
	IPAD_MENU_BLOG="\t\t\t\t\t\t\t\t\t\tblog.siriyang.cn"
	
	IPHONE_MENU_WISHLIST="\t\t\t\t愿望单"
	IPHONE_MENU_FAVORITE="\t\t\t\t收藏夹"
	IPHONE_MENU_UPDATE="\t\t\t    更新数据"
	IPHONE_MENU_SETTING="\t\t\t\t  设置"
	IPHONE_MENU_ABOUT="\t\t\t\t  关于"
	IPHONE_MENU_COPYRIGHT="\t\tCopyright © 2020 by SiriYang. v1.1.1"
	IPHONE_MENU_BLOG="\t\t\t\t\tblog.siriyang.cn"
	
	def __init__(self, app):
		self.app = app
		
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
		
	@ui.in_background
	def loadData(self):
		self.app.activity_indicator.start()
		try:
			menu_listdatasource=None
			if self.app.isIpad():
				menu_listdatasource = ui.ListDataSource(
				[
					{"title": "", "accessory_type": "none"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPAD_MENU_WISHLIST, "accessory_type": "disclosure_indicator","image":"typb:Star"},
					{"title": self.IPAD_MENU_FAVORITE, "accessory_type": "disclosure_indicator","image":"typb:List"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPAD_MENU_UPDATE, "accessory_type": "","image":"typb:Refresh"},
					{"title": self.IPAD_MENU_SETTING, "accessory_type": "disclosure_indicator","image":"typb:Cog"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPAD_MENU_ABOUT, "accessory_type": "none","image":"typb:Info"},
					{"title": "", "accessory_type": "none"},
					{"title": "", "accessory_type": "none"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPAD_MENU_COPYRIGHT, "accessory_type": "none"},
					{"title": self.IPAD_MENU_BLOG, "accessory_type": "none"},
					])
			else:
				menu_listdatasource = ui.ListDataSource(
				[
					{"title": "", "accessory_type": "none"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPHONE_MENU_WISHLIST, "accessory_type": "disclosure_indicator","image":"typb:Star"},
					{"title": self.IPHONE_MENU_FAVORITE, "accessory_type": "disclosure_indicator","image":"typb:List"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPHONE_MENU_UPDATE, "accessory_type": "","image":"typb:Refresh"},
					{"title": self.IPHONE_MENU_SETTING, "accessory_type": "disclosure_indicator","image":"typb:Cog"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPHONE_MENU_ABOUT, "accessory_type": "none","image":"typb:Info"},
					{"title": "", "accessory_type": "none"},
					{"title": "", "accessory_type": "none"},
					{"title": self.IPHONE_MENU_COPYRIGHT, "accessory_type": "none"},
					{"title": self.IPHONE_MENU_BLOG, "accessory_type": "none"},
					])	
			
			menu_listdatasource.action = self.menu_item_tapped
			menu_listdatasource.delete_enabled = False
				
			self.tableView.data_source = menu_listdatasource
			self.tableView.delegate = menu_listdatasource
			self.tableView.reload()
		except Exception as e:
			console.hud_alert('Failed to load menu', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	def loadUI(self):
		pass
	
	def menu_item_tapped(self, sender):
		opt_name = sender.items[sender.selected_row]['title']
		if (opt_name==self.IPAD_MENU_WISHLIST or opt_name==self.IPHONE_MENU_WISHLIST):
			self.WishList_act()
		elif (opt_name==self.IPAD_MENU_FAVORITE or opt_name==self.IPHONE_MENU_FAVORITE):
			self.Favorite_act()
		elif (opt_name==self.IPAD_MENU_UPDATE or opt_name==self.IPHONE_MENU_UPDATE):
			if(self.app.isUpdating):
				console.hud_alert('数据更新中，请稍等！', 'error', 1.0)
				return
				
			console.hud_alert('开始更新中，请稍等！', 'success', 1.0) 
			self.app.isUpdating=True
			self.Update_act()
		elif (opt_name==self.IPAD_MENU_SETTING or opt_name==self.IPHONE_MENU_SETTING):
			self.Setting_act()
		elif (opt_name==self.IPAD_MENU_ABOUT or opt_name==self.IPHONE_MENU_ABOUT):
			self.About_act()
		elif (opt_name==self.IPAD_MENU_BLOG or opt_name==self.IPHONE_MENU_BLOG):
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
		self.nav_view.name = 'AppWishList'
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
