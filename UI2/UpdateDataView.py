# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: UpdateDataView.py
@createTime: 2020-02-02 16:26
@updateTime: 2020-03-29 23:14:28
"""

import ui
import console

from core.AppService import AppService

from tools.Result import *

class UpdateDataView (ui.View):
	
	def __init__(self,app):
		self.app=app
		
		self.index=0
		self.max=1
		
		self.infoLabel=ui.Label()
		self.processionLabel=ui.Label()
		self.percentageLabel=ui.Label()
		
		self.add_subview(self.infoLabel)
		self.add_subview(self.processionLabel)
		self.add_subview(self.percentageLabel)
		
		self.loadUI()
		self.lunch()
		
	def loadUI(self):
		self.name="更新数据"
		self.frame=(0,0,300,150)
		self.background_color="white"
		self.win_w,_=ui.get_window_size()
		if self.win_w>760:
			self.win_w=300
		
		self.infoLabel.text="数据更新中,请等待..."
		self.infoLabel.frame=(0,20,self.win_w,30)
		self.infoLabel.alignment=ui.ALIGN_CENTER
		self.infoLabel.font=("<system>",16)
		
		self.percentageLabel.frame=(20,60,self.win_w-40,40)
		self.percentageLabel.border_width=1
		self.percentageLabel.border_color="#434343"
		self.percentageLabel.text="{f:.2f}%".format(f=(self.index/self.max*100))
		self.percentageLabel.text_color="#d4d4d4"
		self.percentageLabel.alignment=ui.ALIGN_CENTER
		
		self.processionLabel.frame=(20,60,(self.win_w-40)*(self.index/self.max),40)
		self.processionLabel.background_color="#30ba3c"
		
	def updateUI(self):
		self.percentageLabel.text="{f:.2f}%".format(f=(self.index/self.max*100))
		self.processionLabel.width=(self.win_w-40)*(self.index/self.max)
		
	def syndata(self,i,m):
		self.max=max(m,1)
		self.index=min(self.max,i)
		
		self.updateUI()
		
	@ui.in_background
	def lunch(self):
		self.present("sheet",hide_close_button=True)
		
		res=self.app.appService.updateAllApps_Syn(self.syndata)
		
		self.close()
		
		if(not res.equal(ResultEnum.SUCCESS)):
			console.hud_alert('更新出错！', 'error', 1.0)
		else:
			console.hud_alert('更新成功'+str(res.getData()[0])+'个App,失败'+str(res.getData()[1])+'个!', 'success', 2.0)
		
		
if __name__ == "__main__":
	#v=UpdateDataView("../data/")
	pass
	
