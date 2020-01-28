# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: GetJson.py
@time: 2019.12.23 00:04
"""
import requests

def GetHTML(url):
		try:
			r = requests.get(url,timeout=30)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r.text
		except:
			return ""

def GetJson(url):

	html=GetHTML(url)
	jsondata=""
	temp=""

	for i in html.split('\n'):
		if "schema" in i:
			temp=i
			break

	if(temp == ""):
		return None

	for i in range(len(temp)):
		if temp[i] == '>':
			jsondata =temp[i+1:]
			break
		
	return jsondata	
		
def IsJsonValid(jsondic):
	res=jsondic.__contains__("name") and jsondic.__contains__("applicationCategory") and jsondic.__contains__("author") and jsondic.__contains__("offers")
	return res
		
if __name__ == '__main__':
	
	url = "https://apps.apple.com/cn/app/notability/id360593530"
	jsondata=GetJson(url)
	
	print(jsondata)
