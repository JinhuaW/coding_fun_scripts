#!/usr/bin/env python
import re
from mail import *
from mercurial import *
from compile import *
from database import *
import datetime

def update_current_user(db):
	email = get_email()
	username = get_user()
	db.update_user(username, email)


def handle_answer(id, db):
	user = get_user()
	node = get_node()
	path = user + "/" + id
	compile_update(path, node)
	target = get_target(path)
	email = get_email()
	username = get_user()
	
	db.update_user(username, email)

	start_time = datetime.datetime.now()
	result = check_result(path + "/" + target, id)
	end_time = datetime.datetime.now()
	total_time = end_time - start_time
	time_cost = total_time.total_seconds()
	compile_clean(path)
	print "============================================================="
	if result:
		print "Congratulations, success!"
		print "============================================================="
		print "Your result:"
		db.get_rank_time_cost(id, username, time_cost)
		db.update_result(id, email, time_cost, 0)
	else:
		print "You program has failed!"
		print "============================================================="
	print "All result:"
	db.show_rank_time_cost(id)

def handle_exercise(id, db):
	update_current_user(db)	
	diff = get_diff()
	desc = get_desc()
	mail_list = db.get_maillist()
	id = 'N' + id[1:]
	db.update_exercise(id, desc)
	send_mail_plain(diff, "[coding fun]Exercise %s update"%id, mail_from, mail_list)

def update_handle(id, db):
	if id[0] == 'E':
		print "exercise update"
		handle_exercise(id, db)
	elif id[0] == 'N':
		print "handle_answer"
		handle_answer(id, db)
	else:
		print "Unkown Exercise Number"

def check_type():
	desc = get_desc() 
	m = re.match(r'^[EN]\d{8}', desc)
	if m:
		id = m.group()
		return id	
	return None

if __name__ == '__main__':
	id = check_type()
	db=coding_db()
	if id:
		update_handle(id, db)

