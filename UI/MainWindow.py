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

class MainTable(ui.View):
	
	MENU_WISHLIST="\t\t\t\t\t\t\t\t\t愿望单"
	MENU_FAVORITE="\t\t\t\t\t\t\t\t\t收藏夹"
	MENU_UPDATE="\t\t\t\t\t\t\t\t    更新数据"
	MENU_SETTING="\t\t\t\t\t\t\t\t\t  设置"
	MENU_ABOUT="\t\t\t\t\t\t\t\t\t  关于"
	MENU_BLOG="\t\t\t\t\t\t\t\t\t\tblog.siriyang.cn"
	
	def __init__(self, app):
		self.app = app
		
		self.name = '首页'
		self.background_color="white"
		self.flex='WHLRTB'
		
		self.tableView=ui.TableView()
		self.tableView.flex='WHLRTB'
		
		self.add_subview(self.tableView)
		
		self.loadData()
		self.loadUI()
		
	@ui.in_background
	def loadData(self):
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
	
	def loadUI(self):
		pass
	
	def menu_item_tapped(self, sender):
		opt_name = sender.items[sender.selected_row]['title']
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
			res=self.app.appService.updateAllApps()
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert('更新出错！', 'error', 1.0)
			else:
				console.hud_alert('更新成功'+str(len(res.getData()[0]))+'个App,失败'+str(res.getData()[1])+'个!', 'success', 2.0)
				
		except Exception as e:
			console.hud_alert('Failed to update', 'error', 1.0)
		finally:
			self.app.isUpdating=False
	
	def updateData(self):
		self.loadData()
	
	def Setting_act(self):
		pass
		
	def About_act(self):
		webbrowser.open("safari-https://github.com/SiriYXR/AppWishList")
	
	def Blog_act(self):
		webbrowser.open("safari-https://blog.siriyang.cn")

class MainWindow(ui.View):
	
	LANDSCAPE=0
	PORTRAIT=1
	
	def __init__(self,rootpath):
		
		self.rootpath=rootpath
		self.appService=AppService(rootpath)
					
		self.isUpdating=False
		self.orientation = self.LANDSCAPE
								
		self.activity_indicator = ui.ActivityIndicator(flex='LTRB')
		self.activity_indicator.style = 10
		
		self.width,self.height=ui.get_window_size()
		
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
		self.present(style='full_screen',)

if __name__ == '__main__':
	mainWindow = MainWindow("../data/")
	mainWindow.launch()
