# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: CutImage.py
@time: 2020.1.28 16:00
"""

from PIL import Image

def cutImage(path,rect):
	img=Image.open(path)
	
	img=img.crop(rect)
	
	img.save(path)
	
	return img
	
if __name__ == "__main__":
	img=cutImage("../data/img/id407925512.png") 
	img.show()
