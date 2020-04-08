# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: AppsTableView.py
@createTime: 2020-01-29 00:29
@updateTime: 2020-04-08 21:49:02
@codeLines: 235
"""

import ui
import console

from .AppDetailView import AppDetailView
from .SteamPriceLabel import SteamPriceLabel

from core.AppModel import App
from core.AppService import AppService
from core.PriceModel import Price
from core.PriceService import PriceService

from tools.Result import *
from tools.StringProcess import *
from tools.ImgProcess import *

class AppsTableView(ui.View):
	def __init__(self,app,father,name):
		self.app=app
		self.father=father
		
		self.imgStar=ui.Image.named(self.app.rootpath+"UI/img/star_full.PNG")
		self.imgUnStar=ui.Image.named(self.app.rootpath+"UI/img/star_vacancy.PNG")
		
		self.name=name
		self.background_color="white"
		self.flex="WHLRTB"
		
		self.order_key=0
		self.order_desc=0
		self.orderBtn=ui.ButtonItem()
		self.orderBtn.title="收藏时间: 升序"
		self.orderBtn.action=self.order_Act
		self.right_button_items=[self.orderBtn]
					
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
			res=self.app.appService.getAppsByCategory(self.name,self.order_key,self.order_desc)
			
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
		pass		
	
	def layout(self):
		self.tableView.reload()
		pass
	
	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.apps)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.selectable=False
		
		app = self.apps[row]
		cell.text_label.text = StringProcess(app.getName())
		cell.detail_text_label.text = StringProcess(app.getAuthor())
		img=ui.Image.named(self.app.rootpath+"img/"+app.getAppId()+".png")
		if self.app.width<500:
			# iPhone竖屏
			cell.detail_text_label.text = " "
			img=uiImgResize(img,(60,60))
		cell.image_view.image=img
		cell.accessory_type='disclosure_indicator'
	
		self.loadCellItem(cell,app)

		return cell
	
	def loadCellItem(self,cell,app):
		itemView=ui.View()
		itemView.width=300
		itemView.height=50
		
		res=self.app.appService.getPricesByApp(app)
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
		pricelabel.touch_enabled=False
		
		starBtn=ui.Button()
		starBtn.name=app.getAppId() # 利用name属性来记录其对应的app
		starBtn.width=starBtn.height=40
		if(app.getStar()>0):
			starBtn.background_image=self.imgStar
		else:
			starBtn.background_image=self.imgUnStar
		starBtn.action=self.star_Act
		
		autoUpdateBtn=ui.Switch()
		autoUpdateBtn.name=app.getAppId() # 利用name属性来记录其对应的app
		autoUpdateBtn.value=app.getAutoUpdate()
		autoUpdateBtn.tint_color="#0987b4"
		autoUpdateBtn.action=self.changeAutoUpdate_Act
		
		# 设置布局
		pricelabel.x,pricelabel.y=0,10
		starBtn.x,starBtn.y=pricelabel.x+150,pricelabel.y # 以pricelabel为参考系
		autoUpdateBtn.x,autoUpdateBtn.y= starBtn.x+50,starBtn.y+6 # 以starBtn为参考系
		itemView.x=self.tableView.width-300
		if self.app.width<500:
			# iPhone竖屏
			self.tableView.row_height=70
			pricelabel.width=100
			pricelabel.x,pricelabel.y=0,10
			starBtn.width=starBtn.height=30
			starBtn.x,starBtn.y=pricelabel.x+105,pricelabel.y
			autoUpdateBtn.x,autoUpdateBtn.y= starBtn.x+35,starBtn.y-2
			itemView.x,itemView.y=self.tableView.width-230,30
			
		
		itemView.add_subview(pricelabel)
		itemView.add_subview(starBtn)
		itemView.add_subview(autoUpdateBtn)
		cell.content_view.add_subview(itemView)
	
	def tableview_can_delete(self, tableview, section, row):
		return True

	def tableview_can_move(self, tableview, section, row):
		return False
	
	def tableview_title_for_delete_button(self,tableview, section, row):
		return "删除"
	
	@ui.in_background		
	def tableview_did_select(self,tableview, section, row):
		self.app.activity_indicator.start()
		try:
			app = self.apps[row]
			appDetailView = AppDetailView(self.app,self, app)
			self.app.favoriteNavi.push_view(appDetailView)
			self.app.favoriteDeep+=1
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
				
			self.updateData()
		except Exception as e:
			console.hud_alert('Failed to delete Apps', 'error', 1.0)
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
			self.updateData()
			console.hud_alert('刷新成功!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to load renovate', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			
	def updateData(self):
		self.loadData()
		self.father.updateData()
	
	def order_Act(self,sender):
		res=console.alert("排序规则","请选择排序关键字","收藏时间","名称","价格",hide_cancel_button=True)-1
		
		keys=["收藏时间","名称","价格"]
		descs=["升序","降序"]
		
		if res == self.order_key:
			self.order_desc*=-1
			self.order_desc+=1
		else:
			self.order_key=res
			self.order_desc=0
		
		self.orderBtn.title=keys[self.order_key]+": "+descs[self.order_desc]
		
		self.loadData()
		
	def star_Act(self,sender):
		res=self.app.appService.getAppByAppId(sender.name)
		if(not res.isPositive()):
			console.hud_alert('App获取失败!', 'error', 1.0)
			return
		app=res.getData()	
		if(app.getStar()==0):
			self.starApp(app)
		else:
			self.unstarApp(app)	

	def starApp(self,app):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.starApp(app)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('App加入愿望单!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to star App', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			pass

	def unstarApp(self,app):
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.unstarApp(app)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('App已移出愿望单。', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to unstar App', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
			pass	
	
	def changeAutoUpdate_Act(self,sender):
		value=sender.value
		
		self.app.activity_indicator.start()
		try:
			res=self.app.appService.getAppByAppId(sender.name)
			if(not res.isPositive()):
				raise Exception()
				
			res=self.app.appService.changeAppAutoUpdate(res.getData(),value)
			if(not res.isPositive()):
				raise Exception()  
			self.updateData()
			console.hud_alert('App自动更新状态已更改!', 'success', 1.0)
		except Exception as e:
			console.hud_alert('Failed to change App autoupdate', 'error', 1.0)
		finally:
			self.app.activity_indicator.stop()
		
				
			
