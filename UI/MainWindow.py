# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: MainWindow.py
@time: 2020.1.28 18:59
"""

import sys
import ui
import console
import webbrowser

from WishListView import WishListView
from CategoryView import CategoryView

sys.path.append("..")

from AppModel import App
from AppService import AppService

from tools.Result import *

class MainTable(object):
	
	MENU_WISHLIST="\t\t\t\t\t\t\t\t\t愿望单"
	MENU_FAVORITE="\t\t\t\t\t\t\t\t\t收藏夹"
	MENU_UPDATE="\t\t\t\t\t\t\t\t    更新数据"
	MENU_SETTING="\t\t\t\t\t\t\t\t\t  设置"
	MENU_ABOUT="\t\t\t\t\t\t\t\t\t  关于"
	MENU_BLOG="\t\t\t\t\t\t\t\t\t\tblog.siriyang.cn"
	
	def __init__(self, app):
		self.app = app
		
		win_w,win_h=ui.get_window_size()
		self.view = ui.View(frame=(0,0,win_w,win_h))
		self.view.name = '首页'
		self.view.background_color="white"
		self.view.flex='LRTB'
		
		self.tableView=ui.TableView(frame=(0, 0, self.view.width, self.view.height))
		self.view.add_subview(self.tableView)
		
		self.load()
		
	@ui.in_background
	def load(self):
		self.app.activity_indicator.start()
		try:
			menu_listdatasource = ui.ListDataSource(
			[
				{"title": "", "accessory_type": "none"},
				{"title": "", "accessory_type": "none"},
				{"title": self.MENU_WISHLIST, "accessory_type": "disclosure_indicator","image":"typb:Star"},
				{"title": self.MENU_FAVORITE, "accessory_type": "disclosure_indicator","image":"typb:List"},
				{"title": "", "accessory_type": "none"},
				{"title": self.MENU_UPDATE, "accessory_type": "","image":"typb:Refresh"},
				{"title": self.MENU_SETTING, "accessory_type": "disclosure_indicator","image":"typb:Cog"},
				{"title": "", "accessory_type": "none"},
				{"title": self.MENU_ABOUT, "accessory_type": "none","image":"typb:Info"},
				{"title": "", "accessory_type": "none"},
				{"title": "", "accessory_type": "none"},
				{"title": "", "accessory_type": "none"},
				{"title": "\t\t\t\t\t\t\t\t\tCopyright © by SiriYang", "accessory_type": "none"},
				{"title": self.MENU_BLOG, "accessory_type": "none"},
				]
			)
			
			menu_listdatasource.action = self.menu_item_tapped
			menu_listdatasource.delete_enabled = False
				
			self.tableView.data_source = menu_listdatasource
			self.tableView.delegate = menu_listdatasource
			self.tableView.reload()
		except Exception as e:
			console.hud_alert('Failed to load menu', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		
	def menu_item_tapped(self, sender):
		opt_name = sender.items[sender.selected_row]['title']
		if (opt_name==self.MENU_WISHLIST):
			self.WishList_act()
		elif (opt_name==self.MENU_FAVORITE):
			self.Favorite_act()
		elif (opt_name==self.MENU_UPDATE):
			self.Update_act()
		elif (opt_name==self.MENU_SETTING):
			self.Setting_act()
		elif (opt_name==self.MENU_ABOUT):
			self.About_act()
		elif (opt_name==self.MENU_BLOG):
			self.Blog_act()
		
	def WishList_act(self):
		v = WishListView(self.app)
		self.app.nav_view.push_view(v)

	def Favorite_act(self):
		v = CategoryView(self.app)
		self.app.nav_view.push_view(v)

	@ui.in_background
	def Update_act(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.updateAllApps()
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert('更新出错！', 'error', 1.0)
			else:
				console.hud_alert('更新成功'+str(len(res.getData()))+'个App。', 'error', 1.0)
				
		except Exception as e:
			console.hud_alert('Failed to update', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	def Setting_act(self):
		pass
		
	def About_act(self):
		webbrowser.open("safari-https://github.com/SiriYXR/AppWishList")
	
	def Blog_act(self):
		webbrowser.open("safari-https://blog.siriyang.cn")

class MainWindow(object):
	
	def __init__(self,dbpath):
		
		self.appService=AppService(dbpath)
					
		self.activity_indicator = ui.ActivityIndicator(flex='LTRB')
		self.activity_indicator.style = 10
		
		mainTable=MainTable(self)
		self.nav_view=ui.NavigationView(mainTable.view)
		self.nav_view.name = 'AppWishList'
		
		self.nav_view.add_subview(self.activity_indicator)
		self.activity_indicator.frame = (0, 0, self.nav_view.width, self.nav_view.height)
		self.activity_indicator.bring_to_front()
		
	def launch(self):
		self.nav_view.present('fullscreen')

if __name__ == '__main__':
	mainWindow = MainWindow("../data/")
	mainWindow.launch()
