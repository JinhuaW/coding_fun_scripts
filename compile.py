import os 
from mercurial import *
build_repo = "/home/hg/test/coding_fun"

def compile_update(path, node):
	repo_purge(build_repo)
	repo_pull(build_repo)
	repo_update(build_repo, node)
	os.system("make -C " + build_repo + "/" + path)

def compile_clean(path):
	os.system("make clean -C " + build_repo + "/" + path)

def get_target(path):
	fullpath = build_repo + "/" + path + "/Makefile"
	cmd = "echo `sed -ne '{s/^PROGRAM= *\(.*\)$/\\1/p}' " + fullpath + "`"
	m = os.popen(cmd)
	target = m.readline()
	return target.strip()

def check_result(target, id):
	import popen2
	import signal
	def handler(signum, frame):
		raise AssertionError
	signal.signal(signal.SIGALRM, handler)
	input = open(build_repo + "/results/" + id + "/input.txt")
	output = open(build_repo + "/results/" + id + "/output.txt")
	while True:
		try:
		r,w = popen2.popen2(build_repo + "/" + target)
		except Exception, e:
			print "Your program failed:\n  %s" % e.message
			r.close()
			w.close()
			input.close()
			output.close()
			return False
			
		data = input.readline()
		if not data:
			r.close()
			w.close()
			break
		try:
			signal.alarm(3)
			w.write(data)
			w.flush()
			user_result = r.readline()
			signal.alarm(0)
			user_result = user_result.strip()
			standard_result = output.readline()
			standard_result = standard_result.strip()
			if user_result != standard_result:
				input.close()
				output.close()
				return False
		except AssertionError:
			print "Your program failed, it can't finish in 3s"
			r.close()
			w.close()
			input.close()
			output.close()
			return False
	input.close()
	output.close()
	return True
