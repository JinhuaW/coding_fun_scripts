import os

def get_email():
	m = os.popen("hg tip --template '{author|email}\n'")
	email = m.readline()
	email = email.lower()
	return email.strip()

def get_node():
	m = os.popen("hg tip --template '{node}'\n")
	node = m.readline()
	return node.strip()

def get_user():
	m = os.popen("hg tip --template '{author|emailuser}\n'")
	user = m.readline()
	user = user.lower()
	user = user.replace('.', '', len(user))
	return user.strip()

def get_desc():
	m = os.popen("hg tip --template '{desc}\n'")
	desc = m.readline()
	return desc.strip()

def get_diff():
	m = os.popen("hg export tip");
	diff = m.read()
	return diff

def repo_purge(repo):
	cmd = "hg purge --all -R" + ' ' + repo
	result = os.system(cmd)

def repo_update(repo, node):
	cmd = "hg update -C -R" + ' ' + repo + " -r " + node
	result = os.system(cmd)

def repo_pull(repo):
	cmd = "hg pull -u -R" + ' ' + repo
	os.system(cmd)
