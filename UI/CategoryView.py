# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: CategoryView.py
@time: 2020.1.28 21:13
"""
import sys
import ui
import console

from AppsTableView import AppsTableView

sys.path.append("..")

from AppService import AppService

from tools.Result import *

class CategoryView(ui.View):
	
	def __init__(self,app):
		self.app=app
		
		self.name="分类"
		self.background_color="white"
		win_w,win_h=ui.get_window_size()
		self.frame=(0,0,win_w,win_h)
			
		self.tableView = ui.TableView(frame=(0, 0, self.width, self.height))
		self.add_subview(self.tableView)
		
		self.categories_dict = {}
		self.load()
			
	@ui.in_background
	def load(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.getCategories()

			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
				
			self.categories_dict=res.getData() 
			categories_listdatasource = ui.ListDataSource(
				{'title': category_name+" : "+str(self.categories_dict[category_name]), 'accessory_type': 'disclosure_indicator'}
				for category_name in sorted(self.categories_dict.keys())
			)
				
			categories_listdatasource.action = self.category_item_tapped
			categories_listdatasource.delete_enabled = False
				
			self.tableView.data_source = categories_listdatasource
			self.tableView.delegate = categories_listdatasource
			self.tableView.reload()
		#except Exception as e:
			#console.hud_alert('Failed to load Categories', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			
	@ui.in_background
	def category_item_tapped(self, sender):
		self.app.activity_indicator.start()
		try:
			str=sender.items[sender.selected_row]['title']
			category_name = str[:str.find(" : ")]
			apps_table = AppsTableView(self.app, category_name)
			self.app.nav_view.push_view(apps_table)
		except Exception as e:
			console.hud_alert('Failed to load apps list', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
