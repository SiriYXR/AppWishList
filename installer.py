# -*- coding:utf-8 -*-
"""
@author: SiriYang
@file: installer.py
@createTime: 2020-04-05 20:03:25
@updateTime: 2020-04-05 21:39:01
@codeLines: 57
"""

import requests
import sys
import os
import zipfile
import time

URL_BASE='https://raw.githubusercontent.com/SiriYXR/AppWishList/master/archive/'
BASE_DIR=os.path.expanduser('~')
DEFAULT_INSTALL_DIR=os.path.join(BASE_DIR,'Documents/')

def download(url,path):
	print("下载中...: {} ".format(url))
	r=requests.get(url,stream=True)
	file_size=r.headers.get('Content-Length')
	if file_size is not None:
		file_size=int(file_size)
	
	with open(path,'wb') as outs:
		block_sz = 8192
		for chunk in r.iter_content(block_sz):
			outs.write(chunk)
			
def unzip_into(path, outpath, verbose=False):
	"""
	Unzip zipfile at path into outpath.
	:param path: path to zipfile
	:type path: str
	:param outpath: path to extract to
	:type outpath: str
	"""
	if not os.path.exists(outpath):
		os.makedirs(outpath)
	if verbose:
		print('Unzipping into %s ...' % outpath)
		
	with zipfile.ZipFile(path) as zipfp:
		toplevel_directory = None
		namelist = zipfp.namelist()
		
		for name in namelist:
			data = zipfp.read(name)
			fname = os.path.join(outpath, name)
			if fname.endswith('/'):  # A directory
				if not os.path.exists(fname):
					os.makedirs(fname)
			else:
				fp = open(fname, 'wb')
				try:
					fp.write(data)
				finally:
					fp.close()
		
def main():
	starTime=time.time()
	file='AppWishList_v1-2-0.zip'
	url=URL_BASE+file
	zip_path=DEFAULT_INSTALL_DIR+file
	try:
		download(url,zip_path)
		print('下载完成！')
	except:
		print('下载失败!')
		return
	
	print('正在安装 ...')
	
	install_path=DEFAULT_INSTALL_DIR+'AppWishList/'
	zip_file=zipfile.ZipFile(zip_path)
	unzip_into(zip_path,install_path)
	os.remove(zip_path)
	
	print('安装成功！应用已安装到:'+install_path)
	print('耗时: {:.2f}s'.format(time.time()-starTime))

if __name__ == '__main__':
	main()
