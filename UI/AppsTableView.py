# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AppsTableView.py
@time: 2020.1.29 00:29
"""

import sys
import ui
import console

sys.path.append("..")

from AppModel import App
from AppService import AppService

from tools.Result import *

class AppsTableView(ui.View):
	def __init__(self,app,name):
		self.app=app
		
		self.name=name
		self.background_color="white"
		win_w,win_h=ui.get_window_size()
		self.frame=(0,0,win_w,win_h)
			
		self.tableView = ui.TableView(frame=(0, 0, self.width, self.height))
		self.add_subview(self.tableView)
		
		self.load()
		
	@ui.in_background
	def load(self):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.getAppsByCategory(self.name)
			
			if(not res.equal(ResultEnum.SUCCESS)):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
			
			self.apps=res.getData() 
			apps_listdatasource = ui.ListDataSource(
				{'title': app.getName()+"\t\t\t\t\t\t\t\t\t\t"+app.getAuthor(),"image":"../data/img/"+app.getAppId()+".png", 'accessory_type': 'disclosure_indicator'}
				for app in self.apps
			)
			
			apps_listdatasource.action = self.app_item_tapped
			apps_listdatasource.delete_enabled = False
				
			self.tableView.data_source = apps_listdatasource
			self.tableView.delegate = apps_listdatasource
			self.tableView.reload()
		except Exception as e:
			console.hud_alert('Failed to load Apps', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			
	@ui.in_background
	def app_item_tapped(self, sender):
		pass
		
