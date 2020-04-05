# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: LunchMainWin.py
@createTime: 2020-03-28 15:43:34
@updateTime: 2020-04-04 21:27:33
@codeLines: 6
"""

import sys
sys.path.append('.') # 将项目根目录加入模块搜索路径，这样其他模块才能成功导包

from UI2.MainWindow import MainWindow

if __name__ == '__main__':
	mainWindow = MainWindow("./data/")
	mainWindow.launch()
	

