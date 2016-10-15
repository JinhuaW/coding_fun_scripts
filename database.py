#!/usr/bin/env python
import MySQLdb
#import pdb

class database:
	def __init__(self, user_name = 'root', passwd = '2x2=4', db_name='coding_fun', host_name = 'localhost', debug=True):
		self.db = MySQLdb.connect(host_name, user_name, passwd, db_name)
		self.cursor = self.db.cursor()
		self.debug = debug

	def __del__(self):
		if self.db:
			self.db.close()

	def execute(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.trace("MySql excute(%s) failed"%(sql))
			self.db.rollback()
			return False
		return True

	def trace(self, msg):
		if self.debug:
			print msg

class coding_db(database):
	def __drop_table_user(self):
		sql = "drop table user"
		return self.execute(sql)
	
	def __drop_table_result(self):
		sql = "drop table result"
		return self.execute(sql)
	
	def __drop_table_exercise(self):
		sql = "drop table exercise"
		return self.execute(sql) 
	
	def drop_tables(self):
		self.__drop_table_result()
		self.__drop_table_user()
		self.__drop_table_exercise()

	def __create_table_user(self):
		sql = """create table user(
			id int auto_increment primary key,
			enabled boolean default 1,
			name char(64) unique not null,
			email char(128) unique not null,
			reg_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
			)"""
		return self.execute(sql)
	
	def __create_table_result(self):
		sql = """create table result(
			id int auto_increment primary key,
			ex_id int,
			user_id int,
			time_cost float,
			mem_cost float,
			update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
			)"""
		return self.execute(sql)
	
	def __create_table_exercise(self):
		sql = """create table exercise(
			id int auto_increment primary key,
			exercise_id char(16) not null,
			description char(128) null,
			update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
			)"""
		return self.execute(sql) 
			
	def create_tables(self):
		if not self.__create_table_result():
			return False
		if not self.__create_table_user():
			return False
		if not self.__create_table_exercise():
			return False
		return True
				
	def __add_user(self, name, email):
		sql="insert into user(name,email) values('%s','%s')"%(name,email)
		return self.execute(sql)

	def update_user(self, name, email):
		sql="select id from user where email='%s'"%(email)
		if not self.execute(sql):
			return False
		try:
			user_id = self.cursor.fetchone()
			if not user_id:
				return self.__add_user(name, email)
		except:
			return False
		return True

	def show_user(self):
		cut_line = "=" * 83
		inner_line = "-" * 83
		sql="select id,name,email,reg_time from user"
		if not self.execute(sql):
			return False
		try:
			results = self.cursor.fetchall()
			print cut_line 
			print "|%-8s|%-15s|%-35s|%-20s|"%("id","name", "email", "register time")
			print cut_line 
			print inner_line 
			for row in results:
				user_id = row[0]
				name = row[1]
				email = row[2]
				reg_time = row[3]
				print "|%-8d|%-15s|%-35s|%-20s|"%(user_id, name, email, reg_time)
				print inner_line 
			print cut_line 
		except:
			print cut_line 
			return False
		return True
	
	def __add_exercise(self, exercise_id, description):
		sql="insert into exercise(exercise_id, description) values('%s','%s')"%(exercise_id,description)
		return self.execute(sql)

	def __update_exercise(self, ex_id, description):
		sql="update exercise set description='%s' where id = %d"%(description, ex_id)	
		return self.execute(sql)

	def update_exercise(self,exercise_id, description=""):
		sql="select id,exercise_id from exercise where exercise_id='%s'"%(exercise_id)
		if not self.execute(sql):
			return False
		try:
			ex_id = self.cursor.fetchone()
			if not ex_id:
				return self.__add_exercise(exercise_id, description)
			else:
				return self.__update_exercise(ex_id[0], description)
		except:
			return False
		return True
		
	
	def show_exercise(self):
		cut_line = "="*92
		inner_line =  "-"*92
		sql="select id,exercise_id,update_time,description from exercise"
		if not self.execute(sql):
			return False
		try:
			results = self.cursor.fetchall()
			print cut_line
			print "|%-8s|%-19s|%-20s|%-40s|"%("id", "exercise id", "update time", "description")
			print cut_line
			print inner_line
			for row in results:
				ex_id = row[0]
				exercise_id = row[1]
				update_time = row[2]
				desc  = row[3]
				print "|%-8d|%-19s|%-20s|%-40s|"%(ex_id, exercise_id, update_time, desc)
				print inner_line
			print cut_line
		except:
			print cut_line
			return False
		return True

	def __get_user_id(self, email):
		user_id = None
		sql="select id from user where email='%s'"%(email)
		if not self.execute(sql):
			return None
		try:
			user_id = self.cursor.fetchone()
		except:
			return None
		return user_id
	
	def __get_user_name(self, user_id):
		name = None
		sql="select name from user where id=%d"%(user_id)
		if not self.execute(sql):
			return None
		try:
			name = self.cursor.fetchone()
		except:
			return None
		return name 
				
	def __get_ex_id(self, exercise_id):
		ex_id = None
		sql="select id from exercise where exercise_id='%s'"%(exercise_id)
		if not self.execute(sql):
			return None
		try:
			ex_id = self.cursor.fetchone()
		except:
			return None
		return ex_id

	def __get_exercise_id(self, ex_id):
		exercise_id = None
		sql="select exercise_id from exercise where id=%d"%(ex_id)
		if not self.execute(sql):
			return None
		try:
			exercise_id = self.cursor.fetchone()
		except:
			return None
		return exercise_id
	

	def __add_result(self, ex_id, user_id, time_cost, mem_cost):
		sql="insert into result(ex_id, user_id, time_cost, mem_cost) values(%d, %d, %f, %f)"%(ex_id, user_id, time_cost, mem_cost)
		return self.execute(sql)

	def __update_result(self, result_id, time_cost, mem_cost):
		sql="update result set time_cost=%f,mem_cost=%f where id = %d and time_cost > %f"%(time_cost, mem_cost, result_id, time_cost)
		return self.execute(sql)

	def update_result(self, exercise_id, email, time_cost, mem_cost): 		
		ex_id = self.__get_ex_id(exercise_id)
		if not ex_id:
			return False
		
		user_id = self.__get_user_id(email)
		if not user_id:
			return False

		sql = "select id,ex_id,user_id from result where ex_id=%d and user_id=%d"%(ex_id[0], user_id[0])	
		if not self.execute(sql):
			return False

		result_id = self.cursor.fetchone()
		if result_id:
			return self.__update_result(result_id[0], time_cost, mem_cost)	
		else:
			return self.__add_result(ex_id[0], user_id[0], time_cost, mem_cost)

	def show_result(self):
		cut_line = "=" * 74
		inner_line = "-" * 74	
		sql="select id,ex_id,user_id,time_cost,mem_cost,update_time from result"
		if not self.execute(sql):
			return False
		try:
			results = self.cursor.fetchall()
			print cut_line
			print "|%-8s|%-8s|%-8s|%-9s|%-9s|%-25s|"%("id"," ex_id", "user_id", "time cost", " mem cost", " update time")
			print cut_line
			print inner_line
			for row in results:
				id = row[0]
				ex_id = row[1]
				user_id = row[2]
				time_cost = row[3]
				mem_cost = row[4]
				time = row[5] 
				print "|%-8d|%-8d|%-8d|%-9.06f|%-9.03f|%-25s|"%(id, ex_id, user_id, time_cost, mem_cost, time)
				print inner_line
			print cut_line
		except:
			print cut_line
			return False
		return True

	def __show_rank(self, exercise_id, order):
		cut_line = "=" * 76
		inner_line = "-" * 76
		ex_id = self.__get_ex_id(exercise_id)
		if not ex_id:
			print "get exercise_id failed"
			return False
		sql="select user_id,time_cost,mem_cost,update_time from result where ex_id=%d order by %s ASC" %(ex_id[0], order)
		if not self.execute(sql):
			return False
		try:
			results = self.cursor.fetchall()
			print cut_line
			print "|%-6s|%-13s|%-13s|%-13s|%-25s|"%("rank","name", "time cost", "mem cost", " updatetime")
			print cut_line
			print inner_line
			rank = 0
			for row in results:
				user_id = row[0]
				username = self.__get_user_name(user_id)
				if not username:
					print "Database Exception, Unkown user id %d" % user_id
					return False
				time_cost = row[1]
				mem_cost = row[2]
				time = row[3]
				rank = rank + 1 
				print "|%-6d|%-13s|%-9.06f(s)|%-9.03f(kb)|%-25s|"%(rank,username[0], time_cost, mem_cost, time)
				print inner_line
			print cut_line
		except:
			print cut_line
			return False
		return True
	
	def show_rank_time_cost(self, exercise_id, limit=8):
		return self.__show_rank(exercise_id,"time_cost,mem_cost")

	def show_rank_mem_cost(self, exercise_id, limit=8):
		return self.__show_rank(exercise_id, "mem_cost,time_cost")
	
	def show_rank_update_time(self, exercise_id, limit=8):
		return self.__show_rank(exercise_id, "update_time")		


	def get_rank_time_cost(self, exercise_id, username, time_cost):
		cut_line = "=" * 36
		inner_line = "-" * 36 
		ex_id = self.__get_ex_id(exercise_id)
		sql="select count(*) from result where ex_id=%d and time_cost<%f" %(ex_id[0], time_cost)
		if not self.execute(sql):
			return False
		rank = self.cursor.fetchone()
		print cut_line
		print "|%-6s|%-13s|%-12s|"%("rank","name", "time cost")
		print cut_line
		print "|%-6d|%-13s|%-9.06f(s)|"%(rank[0]+1,username, time_cost)
		print cut_line
		return True
			

	def get_rank_mem_cost(self, exercise_id, username, time_cost, mem_cost, time):
		cut_line = "=" * 76
		inner_line = "-" * 76 
		ex_id = self.__get_ex_id(exercise_id)
		sql="select count(*) from result where ex_id=%d and mem_cost<%f" %(ex_id[0], mem_cost)
		if not self.execute(sql):
			return False
		rank = self.cursor.fetchone()
		print cut_line
		print "|%-6s|%-13s|%-13s|%-13s|%-25s|"%("rank","name", "time cost", "mem cost", " updatetime")
		print cut_line
		print "|%-6d|%-13s|%-9.06f(s)|%-9.03f(kb)|%-25s|"%(rank[0] + 1,username, time_cost, mem_cost, time)
		print cut_line
		return True

	def get_rank_update_time(self, exercise_id, username, time_cost, mem_cost, time):
		cut_line = "=" * 76
		inner_line = "-" * 76 
		ex_id = self.__get_ex_id(exercise_id)
		sql="select count(*) from result where ex_id=%d and update_time<'%s'" %(ex_id[0], time)
		if not self.execute(sql):
			return False
		rank = self.cursor.fetchone()
		print cut_line
		print "|%-6s|%-13s|%-13s|%-13s|%-25s|"%("rank","name", "time cost", "mem cost", " updatetime")
		print cut_line
		print "|%-6d|%-13s|%-9.06f(s)|%-9.03f(kb)|%-25s|"%(rank[0] +1,username, time_cost, mem_cost, time)
		print cut_line
		return True

	def get_maillist(self):
		list = ""
		sql="select email,enabled from user"
		if not self.execute(sql):
			return None
		try:
			results = self.cursor.fetchall()
			for row in results:
				email = row[0]
				enabled = row[1]
				if enabled:
					if list:
						list = list + ","
					list = list + email
		except:
			return None
		return list 

#test=coding_db()
#test.drop_tables()
#test.create_tables()
#test.update_user('jinhua','jinhua.wu@alcatel-sbell.com.cn')
#print test.get_maillist()
#test.update_user('a','a@alcatel-sbell.com.cn')
#test.update_user('b','b@alcatel-sbell.com.cn')
#test.show_user()
#test.update_exercise('00000000', "hello")
#test.update_exercise('00000000', "hello.world")
#test.show_exercise()
#test.update_result('00000000', 'jinhua.wu@alcatel-sbell.com.cn', 0.0001, 0.1)
#test.update_result('00000000', 'jinhua.wu@alcatel-sbell.com.cn', 1.0001, 0.1)
#test.update_result('00000000', 'a@alcatel-sbell.com.cn', 0.0012, 0.01)
#test.update_result('00000000', 'b@alcatel-sbell.com.cn', 0.003, 0.09)
#test.show_result()
#test.show_rank_time_cost('00000000')
#test.show_rank_mem_cost('00000000')
#test.show_rank_update_time('00000000')
#test.get_rank_time_cost('00000000', 'jinhua', 0.001)
#test.get_rank_mem_cost('00000000', 'jinhua', 0.001, 0.008, "2016-10-13 19:00:00")
#test.get_rank_update_time('00000000', 'jinhua', 0.001, 0.008, "2016-10-13 19:00:00")
#test.drop_tables()
