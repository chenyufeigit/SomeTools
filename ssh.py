import paramiko
con=paramiko.SSHClient()
con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
con.connect('192.168.12.204',22,'root','gathink')


def com(command):
	stdin,stdout,stderr=con.exec_command(command)
	return stdout.read().strip()
curuser=com('whoami')
hostname=com('hostname')
while True:
	if curuser.strip('\n') == 'root':
		u='#'
	else:
		u='$'
	ps='['+curuser.strip('\n')+'@'+hostname.strip('\n')+':'+'~'+']'+u
	outs=raw_input(ps)
	print(com(outs))
