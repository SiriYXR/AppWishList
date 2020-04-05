# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: ImgProcess.py
@createTime: 2020.1.31 15:11
@updateTime: 2020-04-04 21:21:58
@codeLines: 38
"""

import ui
from PIL import Image
import io
import matplotlib.pyplot
import numpy

def pil2ui(imgIn):
	b = io.BytesIO()
	imgIn.save(b, 'JPEG')
	imgOut = ui.Image.from_data(b.getvalue())
	b.close()
	return imgOut

def ui2pil(ui_img):
	png_data = ui_img.to_png()
	return Image.open(io.BytesIO(png_data))

# 将matplotlib绘制的图像转换成pil图像	
def fig2data(fig):
	
	fig.canvas.draw()
	w,h=fig.canvas.get_width_height()
	buf=numpy.fromstring(fig.canvas.tostring_argb(),dtype=numpy.uint8)
	buf.shape=(w,h,4)
	buf=numpy.roll(buf,3,axis=2)
	return buf
	
def fig2pil(fig):
	buf=fig2data(fig)
	w,h,d=buf.shape
		
	return Image.frombytes("RGBA",(w,h),buf.tostring())

def uiImgResize(imgIn,size):
	if imgIn==None:
		return None
	w,h=size
	imgOut=None
	with ui.ImageContext(w,h) as ctx:
		imgIn.draw(0,0,w,h)
		imgOut=ctx.get_image()
	return imgOut

if __name__ == "__main__":
	uimg=ui.Image.named('../data/img/id360593530.png')
	
	uimg=uiImgResize(uimg,(60,60))
	
	uimg.show()
	
