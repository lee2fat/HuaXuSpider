#-- coding:UTF-8 -*-
from FarChoiceMysql import *
from FarChoiceSqlite3 import *


class FarChoiceDBFactory(object):	
	@staticmethod
	def Create( which):
		if which == "mysql":
			return FarChoiceMysql()
		elif which == "sqlite3":
			return FarChoiceSqlite3()
		else:
			return None




