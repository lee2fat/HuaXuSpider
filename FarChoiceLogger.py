#-- coding:UTF-8 -*-
import logging
from logging.handlers import RotatingFileHandler


class FarChoiceRotatingLogger(object):
	"""
	可修改的配置 开始
	"""
	#定义一个RotatingFileHandler，最多备份10个日志文件，每个日志文件最大1M
	logfilename = "hxlog.txt"
	maxBytes = 1024 * 1024 
	backupCount = 16 

	level = logging.INFO

	"""
	可修改的配置 结束，下面代码勿随意修改
	"""
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(level = self.level)  #logging.INFO  | logging.DEBUG
		
		rHandler = RotatingFileHandler(filename = self.logfilename, maxBytes = self.maxBytes,	backupCount = self.backupCount)

		rHandler.setLevel(self.level)	
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		rHandler.setFormatter(formatter)

		self.logger.addHandler(rHandler) 
		

	def __str__(self):
		return "FarChoiceRotatingLogger"


	def info(self, str):
		self.logger.info(str)
		
	def debug(self, str):
		self.logger.debug(str)

	def warning(self, str):
		self.logger.warning(str)

	def error(self, str):
		self.logger.error(str)

	def critical(self, str):
		self.logger.critical(str)

	