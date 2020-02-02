# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: AlertView.py
@time: 2020.2.2 13:44
"""

import ui

class AlertView (ui.View):
	
	def __init__(self,title="Alert",info="",act=None):
		self.value=0
		self.act=act
		
		self.name=title
		self.frame=(0,0,250,120)
		self.background_color="white"
		
		self.infoLabel=ui.TextView()
		self.infoLabel.text=info
		self.infoLabel.font=("<system>",16)
		self.infoLabel.text_color="#5a5a5a"
		self.infoLabel.alignment=ui.ALIGN_CENTER
		self.infoLabel.frame=(0,20,self.width,self.height-50-20)
		
		self.okBtn=ui.Button()
		self.okBtn.title="确定"
		self.okBtn.border_width=1
		self.okBtn.frame=(-1,self.height-50,self.width/2+1,50+1)
		self.okBtn.background_color="white"
		self.okBtn.border_color="#eaeaea"
		#self.okBtn.corner_radius=5
		self.okBtn.action=self.okAct
		
		self.closeBtn=ui.Button()
		self.closeBtn.title="取消"
		self.closeBtn.border_width=1
		self.closeBtn.frame=(self.width/2,self.height-50,self.width/2,50+1)
		self.closeBtn.background_color="white"
		self.closeBtn.border_color="#eaeaea"
		#self.closeBtn.corner_radius=5
		self.closeBtn.action=self.closeAct
		
		self.add_subview(self.infoLabel)
		self.add_subview(self.okBtn)
		self.add_subview(self.closeBtn)
		
		self.present("sheet")
		
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
	
