# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: MainWindow.py
@createTime: 2020-04-04 18:01:06
@updateTime: 2020-04-05 00:20:48
@codeLines: 170
"""

import ui
import console

from .WishListView import WishListView
from .CategoryView import CategoryView
from .SettingView import SettingView

from core.AppModel import App
from core.AppService import AppService
from core.ConfigService import ConfigService

class MainWindow(ui.View):
	
	LANDSCAPE=0
	PORTRAIT=1
	
	IPAD=0
	IPHONE=1
	
	NORMAL=0
	TEST_IPHOE_L=1
	TEST_IPHOE_P=2
	
	STAR=0
	FAVORITE=1
	MORE=2
	
	BTN_ON_COLOR='#27a2f1'
	BTN_OFF_COLOR='#8e8e8e'
	
	def __init__(self,rootpath,test_mod=0):
		self.name = 'AppWishList'
		self.rootpath=rootpath
		self.appService=AppService(rootpath)
		self.configService=ConfigService(rootpath)
		
		self.orientation = self.LANDSCAPE
		self.divice=self.IPAD
		self.test_mod=test_mod
		self.isUpdating=False
					
		self.viewKind=self.STAR
		self.starDeep=0
		self.favoriteDeep=0
		self.moreDeep=0
					
		if self.test_mod==self.NORMAL:
			self.width,self.height=ui.get_window_size()
		elif self.test_mod==self.TEST_IPHOE_P:
			# iPhone test
			self.width,self.height=414,736
		else:
			self.width,self.height=736,414
		if(self.width+self.height<1024+768):
			self.divice=self.IPHONE
		
		self.activity_indicator = ui.ActivityIndicator(flex='LTRB')
		self.activity_indicator.style = ui.ACTIVITY_INDICATOR_STYLE_GRAY
		
		self.starView=WishListView(self)
		self.favoriteView=CategoryView(self)
		self.moreView=SettingView(self)
		self.starNavi=ui.NavigationView(self.starView)
		self.favoriteNavi=ui.NavigationView(self.favoriteView)
		self.moreNavi=ui.NavigationView(self.moreView)
		
		self.bottomView=ui.View()
		self.starBtn=ui.Button()
		self.favoriteBtn=ui.Button()
		self.moreBtn=ui.Button()
		
		self.bottomView.add_subview(self.starBtn)
		self.bottomView.add_subview(self.favoriteBtn)
		self.bottomView.add_subview(self.moreBtn)
		
		self.add_subview(self.starNavi)
		self.add_subview(self.favoriteNavi)
		self.add_subview(self.moreNavi)
		self.add_subview(self.bottomView)
		self.add_subview(self.activity_indicator)
		
		self.loadUI()
		
		self.activity_indicator.bring_to_front()
		
	def loadUI(self):
		self.favoriteNavi.hidden=True
		self.moreNavi.hidden=True
		
		self.bottomView.background_color='#f1f1f1'
		
		self.starBtn.image=ui.Image.named('iob:ios7_star_32')
		self.starBtn.title='愿望单'
		self.starBtn.action=self.Star_act
		self.starBtn.tint_color=self.BTN_ON_COLOR
		
		self.favoriteBtn.image=ui.Image.named('iob:filing_32')
		self.favoriteBtn.title='收藏夹'
		self.favoriteBtn.action=self.Favorite_act
		self.favoriteBtn.tint_color=self.BTN_OFF_COLOR
		
		self.moreBtn.image=ui.Image.named('iob:ios7_more_outline_32')
		self.moreBtn.title='更多'
		self.moreBtn.action=self.More_act
		self.moreBtn.tint_color=self.BTN_OFF_COLOR
	
	def layout(self):
		if self.width > self.height:
			self.orientation=self.LANDSCAPE
		else:
			self.orientation=self.PORTRAIT
		
		bottomView_h=50
		if (not self.isIpad()):
			bottomView_h=60
			
		self.starNavi.frame=(0,0,self.width,self.height-bottomView_h)
		self.favoriteNavi.frame=(0,0,self.width,self.height-bottomView_h)
		self.moreNavi.frame=(0,0,self.width,self.height-bottomView_h)
			
		self.bottomView.frame=(0,self.height-bottomView_h,self.width,bottomView_h)
		
		margin=(self.width-300)/4
		self.starBtn.frame=(margin,0,100,50)
		self.favoriteBtn.frame=(margin*2+100,0,100,50)
		self.moreBtn.frame=(margin*3+200,0,100,50)
		
	def launch(self):
		if self.test_mod==self.NORMAL:
			self.present(style='fullscreen',hide_title_bar=True)
		else:
			self.present(style='sheet',hide_title_bar=True)

	def isIpad(self):
		return self.divice==self.IPAD
		
	def Star_act(self,sender):
		if self.viewKind==self.STAR:
			return
		self.activity_indicator.start()
		try:
			self.starView.updateData()
			self.starNavi.hidden=False
			self.favoriteNavi.hidden=True
			self.moreNavi.hidden=True
			for i in range(self.favoriteDeep):
				self.favoriteNavi.pop_view()
			for i in range(self.moreDeep):
				self.moreNavi.pop_view()
		except Exception as e:
			console.hud_alert('愿望单页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind=self.STAR
			self.starBtn.tint_color=self.BTN_ON_COLOR
			self.favoriteBtn.tint_color=self.BTN_OFF_COLOR
			self.moreBtn.tint_color=self.BTN_OFF_COLOR
			self.activity_indicator.stop()
			
	def Favorite_act(self,sender):
		if self.viewKind==self.FAVORITE:
			return
		self.activity_indicator.start()
		try:
			self.favoriteView.updateData()
			self.favoriteNavi.hidden=False
			self.starNavi.hidden=True
			self.moreNavi.hidden=True
			for i in range(self.starDeep):
				self.starNavi.pop_view()
			for i in range(self.moreDeep):
				self.moreNavi.pop_view()
		except Exception as e:
			console.hud_alert('收藏夹页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind=self.FAVORITE
			self.starBtn.tint_color=self.BTN_OFF_COLOR
			self.favoriteBtn.tint_color=self.BTN_ON_COLOR
			self.moreBtn.tint_color=self.BTN_OFF_COLOR
			self.activity_indicator.stop()
			
	def More_act(self,sender):
		if self.viewKind==self.MORE:
			return
		self.activity_indicator.start()
		try:
			self.moreView.updateData()
			self.moreNavi.hidden=False
			self.starNavi.hidden=True
			self.favoriteNavi.hidden=True
			for i in range(self.starDeep):
				self.starNavi.pop_view()
			for i in range(self.favoriteDeep):
				self.favoriteNavi.pop_view()
		except Exception as e:
			console.hud_alert('更多设置页面加载失败！', 'error', 1.0)
		finally:
			self.viewKind=self.MORE
			self.starBtn.tint_color=self.BTN_OFF_COLOR
			self.favoriteBtn.tint_color=self.BTN_OFF_COLOR
			self.moreBtn.tint_color=self.BTN_ON_COLOR
			self.activity_indicator.stop()
			
	def Close_act(self,sender):
		self.close()
		
if __name__=="__main__":
	pass
