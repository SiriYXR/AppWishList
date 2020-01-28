# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: DownLoadImage.py
@time: 2019.12.24 22:51
"""
import requests

def downLoadImage(url,path):
	r=requests.get(url)
	
	with open(path,'wb') as f:
		f.write(r.content)
		f.flush()
		f.close()
		
if __name__ == "__main__":
	downLoadImage('https://is1-ssl.mzstatic.com/image/thumb/Purple113/v4/62/59/0f/62590f70-e329-637d-b7be-ad5a13174352/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png','../data/img/i.png')	
