#-- coding:UTF-8 -*-
import time
import json
import math
from datetime import datetime

from FarChoiceLogger import *
from FarChoiceDBFactory import *
from PiaoXinWangPage import *


#网页上的合法值 = {10,20,30,40,50,100}
minitemsperpage = 10
maxitemsperpage = 100


def HandleAllItems(logger, db, items):
	db.deletelast()
	now = datetime.now()
	for item in items:  #  items 有重复数据的可能，暂时不错处理
		db.insertlast(item, now)
		db.updatehistory(item, now)
	db.commit()

def GetPagesEx(logger, db):
	listpage = PiaoXinWangListPage(logger)

	curr = 1
	code, total, allitems = listpage.getitems(maxitemsperpage, curr)
	curr = curr + 1

	if code == 0 :
		times = math.ceil(total / maxitemsperpage )

		while curr <= times :
			logger.debug(curr)			
			code, total, items = listpage.getitems(maxitemsperpage, curr)
			curr = curr + 1
			#time.sleep(0.1)

			if code == 0 :
				allitems.extend(items)  
			elif code == -1 :
				logger.info("HTTP网络请求格式错误")
			elif code == -2:
				logger.info("HTTP请求超时异常")
			else :
				logger.info("未知错误 code = %d" % code)

		HandleAllItems(logger, db, allitems)
	elif code == -1 :
		logger.info("HTTP网络请求格式错误")
	elif code == -2:
		logger.info("HTTP请求超时异常")
	else :
		logger.info("未知错误 code = %d" % code)
	return code 

def cycle(delayseconds):
	while True:
		GetPagesEx(logger , db)
		logger.info("脚本睡眠 %d 秒" % (delayseconds))
		time.sleep(delayseconds)


if __name__ == '__main__':	
	#初始化
	logger = FarChoiceRotatingLogger()
	db = FarChoiceDBFactory.Create("mysql")
	db.initdb(logger)
	
	logger.info("********************************************************") #日志分割线
	logger.info("启动脚本，选择了%s存储数据" % (str(db)))
	
	cycle(delayseconds = 10)		#主循环体
	
	logger.info("结束脚本") 		#结束日志，目前不会打印下面这条

	pass

