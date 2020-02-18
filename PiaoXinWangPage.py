#-- coding:UTF-8 -*-
import http.client
import json

class PiaoXinWangListPage(object):

	#list请求是向下面域名请求的
	host = "mtapi.sdpjw.cn" 
	method = "POST"
	path = "/api/draft/list"
	
	requestbodyformat = '{"size":%d,"current":%d,"todayFlag":1,"channel":1}'

	headers = {
			 "Origin": "http://vip.piaoxinwang.com"
			,"Referer": "http://vip.piaoxinwang.com/"
			,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
			,"Accept": "application/json, text/plain, */*"
			,"Content-Type": "application/json;charset=UTF-8"
			}
	###########################################
	timeout = 30 			# 5秒超时

	def __init__(self, logger):
		self.logger = logger
		pass

	def __str__(self):
		pass

	def getitems(self, sz, curr):
		# 返回值 code , total , items 
		# code < 0 ,失败
		try:
			body = self.requestbodyformat % (sz, curr)
		
			conn = http.client.HTTPConnection(self.host, timeout = self.timeout)

			conn.request(self.method, self.path, body, self.headers)
			res = conn.getresponse()

			data = res.read()
			jdata = json.loads(data)

			self.logger.debug(jdata)

			code = jdata['code']

			if code == 0 :
				total = jdata['page']['totalCount']
				items = jdata['page']['list']			
				return code, total, items 
			else :
				if code == 500:
					code = -1				
				return code, 0, None
		except :
			# 超时 
			return -2, None, None
		finally:
			self.logger.debug("finally")
			conn.close() 


