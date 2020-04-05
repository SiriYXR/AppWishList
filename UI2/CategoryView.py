# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: CategoryView.py
@createTime: 2020-01-28 21:13
@updateTime: 2020-04-04 21:27:58
@codeLines: 112
"""

import ui
import console

from .AppsTableView import AppsTableView

from core.AppService import AppService

from tools.Result import *

class CategoryView(ui.View):
	
	def __init__(self,app):
		self.app=app
		
		self.name="分类"
		self.background_color="white"
		self.flex="WHLRTB"
		
		self.closeBtn=ui.ButtonItem()
		self.closeBtn.image=ui.Image.named('iob:close_round_24')
		self.closeBtn.action=self.app.Close_act
		self.left_button_items=[self.closeBtn]
		
		self.tableView = ui.TableView()
		if self.app.isIpad():
			self.tableView.width=710
		else:
			self.tableView.width=414
		self.tableView.y=0
		self.add_subview(self.tableView)
		
		self.categories_dict = {}
		self.categories_names = []
		
		self.tableView.data_source = self
		self.tableView.delegate = self		
		
		self.loadData()
	
	def loadData(self):
		try:
			res=self.app.appService.getCategories()

			if(not res.isPositive()):
				console.hud_alert(res.toString(), 'error', 1.0)
				return 
				
			self.categories_dict=res.getData() 
			self.categories_names = sorted(self.categories_dict.keys())
			
			self.tableView.reload()

		except Exception as e:
			console.hud_alert('Failed to load Categories_Dict', 'error', 1.0)
		finally:
			pass
	
	def layout(self):
		self.tableView.reload()
		
		# tabelView手动居中
		self.tableView.height=self.height
		self.tableView.x=(self.width-self.tableView.width)/2
	
	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.categories_dict)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		categories_name = self.categories_names[row]
		categories_count = self.categories_dict[categories_name]
		cell.text_label.text = categories_name
		cell.accessory_type='disclosure_indicator'
		cell.selectable=False
		
		label=ui.Label()
		label.frame=(self.tableView.width-100,10,50,25)
		label.alignment=ui.ALIGN_CENTER
		label.border_width = 1
		label.corner_radius=5
		label.background_color="white"
		label.text_color="#9400d3"
		label.border_color="#9400d3"
		label.text=str(categories_count)
		
		cell.content_view.add_subview(label)
		
		return cell

	def tableview_can_delete(self, tableview, section, row):
		return True

	def tableview_can_move(self, tableview, section, row):
		return False
	
	@ui.in_background		
	def tableview_did_select(self,tableview, section, row):
		self.app.activity_indicator.start()
		try:
			category_name = self.categories_names[row]
			apps_table = AppsTableView(self.app,self, category_name)
			self.app.favoriteNavi.push_view(apps_table)
			self.app.favoriteDeep+=1
		#except Exception as e:
			#console.hud_alert('Failed to load apps list', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
	
	def tableview_title_for_delete_button(self,tableview, section, row):
		return "删除"
		
	def tableview_delete(self,tableview, section, row):
		category=self.categories_names[row]
			
		res=console.alert("删除分类",'你确定要删除"'+category+'"分类及其下所有App吗？',"确定","取消",hide_cancel_button=True)
		
		if(res==1):
			self.deleteCategory(category)	
	
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
			console.hud_alert('Failed to load Categories_Dict', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()	
			
	def updateData(self):
		self.loadData()
		
	def deleteCategory(self,category):
		self.app.activity_indicator.start()
		try:
			self.app.appService.deleteAppsByCategory(category)
			self.loadData()
		except Exception as e:
			console.hud_alert('Failed to delete category', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
