#-- coding:UTF-8 -*-
from FarChoiceLogger import *
from datetime import datetime

import sqlite3
import os.path
import hashlib

class FarChoiceSqlite3(object):
	"""
	"""
	filename = "Tickets.db"

	"""
	"""
	def __init__(self):
		pass

	def __str__(self):		
		return "sqlite3"

	def initdb(self, logger):
		self.logger = logger

		exist = os.path.isfile(self.filename)
		self.conn = sqlite3.connect(self.filename)

		with self.conn:
			self.lastcursor = self.conn.cursor()
			self.historycursor = self.conn.cursor()
			if exist is not True :
				self.lastcursor.execute("CREATE TABLE LastTickets\
					        (id  TEXT PRIMARY KEY,\
							 publishDate	TEXT ,\
					       	 getDate      	TEXT ,\
					         acceptance   	TEXT ,\
					         draftAmt  		TEXT ,\
					         expiryDate     TEXT ,\
							 discountDays	TEXT ,\
					         lakhFee 		TEXT ,\
					         annualInterest TEXT ,\
					         flaw 		  	TEXT ,\
					         fee		  	TEXT ,\
					         imgurls		TEXT ,\
					         md5			TEXT,\
					         draftType		INT\
					         );")

				self.historycursor.execute("CREATE TABLE HistoryTickets\
					        (id  TEXT ,\
							 publishDate	TEXT ,\
					       	 getDate      	TEXT ,\
					         acceptance   	TEXT ,\
					         draftAmt  		TEXT ,\
					         expiryDate     TEXT ,\
							 discountDays	TEXT ,\
					         lakhFee 		TEXT ,\
					         annualInterest TEXT ,\
					         flaw 		  	TEXT ,\
					         fee		  	TEXT ,\
					         imgurls		TEXT ,\
					         md5 TEXT PRIMARY KEY,\
					         draftType		INT\
					         );")

			return 0
		return -1

	def deletelast(self):
		try:
			self.logger.debug("delete LastTickets")
			self.lastcursor.execute("DELETE FROM LastTickets")
		except  (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
			self.logger.info(e)

	def insertlast(self, item, now):
		md5 = self.item2md5(item)
		try:
			self.logger.debug("insert %s"  % (str(item)))

			self.lastcursor.execute("insert into LastTickets\
				(id,  			publishDate, 	getDate, 		acceptance, \
				draftAmt, 		expiryDate, 	discountDays, 	lakhFee, \
				annualInterest, flaw, 			fee, 			imgurls,\
				md5 ,draftType)\
				values('{}','{}','{}','{}',\
				'{}','{}','{}','{}',\
				'{}','{}','{}','{}',\
				'{}', '{}')"\
				.format(item['id'], item['publishDate'], now , item['acceptance'], \
				 item['draftAmt'], item['expiryDate'], item['discountDays'], item['lakhFee'], \
				 item['annualInterest'], item['flaw'], "", "", md5, item['draftType']))
			self.conn.commit()		
		except  (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
			self.logger.info(e)
		pass
	def item2md5(self,item):
		total = str(item['id']) + str(item['publishDate']) + str(item['acceptance'])+ \
			str(item['draftAmt'])+str(item['expiryDate'])+str(item['discountDays'])+str(item['lakhFee']) + \
			str(item['annualInterest']) + str(item['flaw'])+ "" + "" + str(item['draftType'])

		return hashlib.md5(total.encode("utf-8")).hexdigest()

	def updatehistory(self, item, now):		
		try:
			self.logger.debug("updatehistory %s" % (str(item)))

			md5 = self.item2md5(item)
			selectsql = "select * from HistoryTickets where md5 = '%s'" % (md5)
			self.historycursor.execute(selectsql)

			if len(list(self.historycursor)) > 0 :
				self.logger.debug("数据重复，啥也不做 md5:"+ md5)
			else :
				self.logger.info("数据不存在，插入 md5:"+ md5)
				self.historycursor.execute("insert into HistoryTickets\
					(id,  			publishDate, 	getDate, 		acceptance, \
					draftAmt, 		expiryDate, 	discountDays, 	lakhFee, \
					annualInterest, flaw, 			fee, 			imgurls ,\
					md5, 			draftType)\
					values('{}','{}','{}','{}',\
					'{}','{}','{}','{}',\
					'{}','{}','{}','{}',\
					'{}','{}')"\
					.format(item['id'], item['publishDate'], now , item['acceptance'], \
					 item['draftAmt'], item['expiryDate'], item['discountDays'], item['lakhFee'], \
					 item['annualInterest'], item['flaw'], "", "" , md5, item['draftType']))					
		except  (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
			self.logger.info(e)
		pass

	def close(self):
		self.lastcursor.close()
		self.historycursor.close()
		self.conn.close()

	def commit(self):
		self.conn.commit()	
		
