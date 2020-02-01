# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: ImgProcess.py
@time: 2020.1.31 15:11
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
	
if __name__ == "__main__":
	figure=matplotlib.pyplot.figure()
	plot=figure.add_subplot(111)
	x = numpy.arange(1,100,0.1)
	y = numpy.sin(x)/x
	plot.plot(x,y)
	
	i=pil2ui(fig2pil(figure))
	
	v=ui.ImageView()
	
	v.frame=(0,0,1000,600)
	v.background_color="white"
	
	v.image = i
	
	v.present("sheet")
