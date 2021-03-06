# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: AlertView.py
@createTime: 2020.2.2 13:44
@updateTime: 2020-03-31 23:55:56
@codeLines: 56
"""

import ui

class AlertView (ui.View):
	
	def __init__(self,title="Alert",info="",act=None):
		self.value=0
		self.act=act
		
		self.frame=(0,0,250,180)
		self.background_color="white"
		self.win_w,self.win_h=ui.get_window_size()
		self.win_h-=50
		if self.win_w>760:
			self.win_w=250
			self.win_h=180
		
		self.titleLabel=ui.Label()
		self.titleLabel.text=title
		self.titleLabel.font=("<system>",20)
		self.titleLabel.text_color="#000"
		self.titleLabel.alignment=ui.ALIGN_CENTER
		self.titleLabel.frame=(0,20,self.win_w,20)
		
		self.infoLabel=ui.Label()
		self.infoLabel.text=info
		self.infoLabel.font=("<system>",16)
		self.infoLabel.text_color="#5a5a5a"
		self.infoLabel.alignment=ui.ALIGN_CENTER
		self.infoLabel.frame=(0,self.titleLabel.height,self.win_w,self.win_h-self.titleLabel.height-50)
		
		self.okBtn=ui.Button()
		self.okBtn.title="确定"
		self.okBtn.border_width=1
		self.okBtn.frame=(-1,self.win_h-50,self.win_w/2+1,50+1)
		self.okBtn.background_color="white"
		self.okBtn.border_color="#eaeaea"
		#self.okBtn.corner_radius=5
		self.okBtn.action=self.okAct
		
		self.closeBtn=ui.Button()
		self.closeBtn.title="取消"
		self.closeBtn.border_width=1
		self.closeBtn.frame=(self.win_w/2,self.win_h-50,self.win_w/2,50+1)
		self.closeBtn.background_color="white"
		self.closeBtn.border_color="#eaeaea"
		#self.closeBtn.corner_radius=5
		self.closeBtn.action=self.closeAct
		
		self.add_subview(self.titleLabel)
		self.add_subview(self.infoLabel)
		self.add_subview(self.okBtn)
		self.add_subview(self.closeBtn)
		
		self.present("sheet",hide_title_bar=True)
		self.wait_modal()
		
	def will_close(self):
		pass
	
	def okAct(self,sender):
		self.value=1
		if(self.act!=None):
			self.act()
		self.close()
	
	def closeAct(self,sender):
		self.value=0
		self.close()		
		
if __name__ == "__main__":
	v=AlertView("test","123456")
	
