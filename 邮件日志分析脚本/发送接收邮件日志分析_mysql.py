#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os,sys
import subprocess
import shlex
import signal
import MySQLdb
import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='/var/log/sendrecvmaillog.log',
                filemode='a')

def logInfo(level,msg):
    if level == 'info':
        logging.info(msg)
    elif level == 'warning' or level == 'warn':
        logging.warning(msg)
    elif level == 'debug':
        logging.debug(msg)
    elif level == 'error':
        logging.error(msg)
    else:
        logging.error('loglevel is error')

def subKill(a,b):
    try:
        os.kill(spid,15)
        logInfo('error','killed')
    except:
        logInfo('error','kill subproc is Failure')
    sys.exit(15)

def getMileInfo(m):
    status = '其它(暂时性错误)'
    sdict={'status\=sent':'成功',
'sender policies found':'找到多余的适用发件人策略',
'Missing required IPv4 address':'缺少必要的IP地址',
'Unknown mechanism type':'未知的类型TXT记录',
'Maximum void DNS look\-ups limit':'超过最大dns术语限制',
'Maximum DNS-interactive terms limit':'超过最大dns术语限制',
'Junk encountered in mechanism':'垃圾邮件',
'Junk encountered in record':'垃圾邮件',
'Maximum void DNS look\-ups limit':'超过最大dns查询限制',
'need fully\-qualified hostname':'需要是完全合格域名',
'blocked using zen\.spamhaus\.org':'邮件地址或ip被加入zen.spamhaus.org黑名单访问https://mxtoolbox.com/domain/',
'Sender address rejected':'发件人地址被拒绝',
'Sender address rejected\: SPF-Result':'对方SPF,txt记录错误',
'Sender address rejected\: Domain not found':'域名未发现',
'Sender address rejected\: not logged in':'Outlook未勾选smtp需要验证',
'Recipient address rejected':'收人人地址拒绝(需要加白名单)',
'said\: 550 [Mm]ailbox':'收件人未找到(用户可能不存在)',
'said\: 550 Domain frequency limited':'域名发信限制(发邮件太频繁)',
'said\: 55[3-4]':'垃圾邮件',
'[uU]ser not exist':'用户不存在',
'said\: 550 User suspended':'邮箱暂停使用',
'said\: 550 User not found':'用户未找到',
'said\: 550 Mailbox not found':'没有收件箱',
'said\: 451 temporary failure for one or more recipients':'一个或多个收件人临时失败',
'Connection timed out':'连接对方服务器超时',
'lost connection':'与对方失去连接',
'[rR]elay access denied':'中继访问拒绝',           
'Message rejected as spam by Content Filterin':'邮件内容被视为垃圾邮件(加白名单)',
'said\: 550 No [sS]uch [uU]ser':'用户不存在',
'Email address could not be found':'地址不存在',
'does not exist here':'收件人不存在',
'Connection refused':'连接被拒绝',
'said: 422 ERR.LOGIN.USERSTATUS':'错误用户登录状态',
'Please try again later':'请稍后再试',
'said: 501 Bad address syntax':'地址语法错误',
'Undelivered Mail 550 Returned to Sender':'未送达邮件已返回发件人',
'Host not found':'邮件域名未找到',
'INFECTED':'感染病毒',
'[Uu]ser [uU]nknown':'未知用户',
'timed out while receiving the initial server greeting':'接收初始服务器问候语时超时',
'Mail content denied':'邮件内容被拒绝',
'Spam message is rejected':'垃圾邮件',
'Requested action not taken':'请求未执行',
'Quota exceeded or service disabled':'超出配额或服务禁用',
'Mail is rejected by recipients':'邮件被收件人拒绝',
'relaying denied':'拒绝中继',
'Recipient not found':'收件人未找到',
'No route to host':'没有路由到主机',
'[uU]nknown [Uu]ser':'未知用户'}
    mid, nt, n = '', '', ''
    ser, sip = '不能解析服务器', '未知'
    mailre = re.compile(r'[^\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    timere = re.compile(r'^\w+\s+\d+\s\d{2}\:\d{2}:\d{2}')
    mailserver = re.compile(r'relay=(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]|relay=(?:[A-Za-z0-9-_]+\.)+[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]|relay=local')
    mid = re.search(r'\w{12}:',m)
    if mid is not None:
        mid = mid.group().rstrip(':')
    nt = timere.search(m)
    if nt is not None:
        nt = nt.group()
    n = mailre.search(m)
    mserverinfo = mailserver.search(m)
    if mserverinfo is not None:
        info = re.search(r'(?:[A-Za-z0-9-_]+\.)+[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|local',mserverinfo.group())
        if info is not None:
	    infog=info.group()
	    if infog is not None and infog != 'local':
                ser, sip = infog.split(r'[')
            if infog == 'local':
                ser = 'local' 
	        sip = 'local'
    if n is not None:
        recvaddr = n.group().strip('<')
    for key in sdict:
        statre = re.search(key,m)
        if statre is not None:
            status = sdict[key]
        else:
            pass
    logInfo('info','ID:%s MAILTO:%s STATUS:%s' % (mid,recvaddr,status))
    sendtime = formatTime(nt)
    recvaddr = sendrecvjoin(recvaddr)
    sql = "insert into real_mail_log(send_time,mail_id,recv_mail_addr,server_domain,server_ip,mail_status) values('%s','%s','%s','%s','%s','%s')" % (sendtime,mid,recvaddr,ser,sip,status)
    insertMail(sql)
#    print >>sys.stdout,("SQL: insert into real_maill_log(send_time,mail_id,recv_mail_addr,server_domain,server_ip,mail_status) values('%s','%s','%s','%s','%s','%s')" % (sendtime,mid,recvaddr,ser,sip,status))

#提取amavis的信息
def getamavisInfo(m):
    status = 'amavis其它(未知错误)'
    sdict={'Passed CLEAN':'amavis检查_通过',
           'Passed BAD-HEADER':'邮件头部错误_通过',
           'Passed SPAMMY':'快成为垃圾邮件_通过',
           'Blocked SPAM':'垃圾邮件_不通过',
           'Blocked INFECTED':'病毒邮件_不通过'
           }

    #提取对方服务器地址
    mailserver = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    #提取邮件账号
    mailre = re.compile(r'[^<\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    timere = re.compile(r'^\w+\s+\d+\s\d{2}\:\d{2}:\d{2}')
    filenamere = re.compile(r'quarantine\: [\w\.-]+')
    nt = timere.search(m)
    sip = mailserver.search(m).group()
    if nt is not None:
        nt = nt.group()
    #amavis中第一个是发件人，之后的是收件人（不包含最后一个系统的）n是发、收件人列表
    n = mailre.findall(m)
    if n is not None:
        try:
            sendaddr=n[0]
            ser = n[0].split('@')[1]
        except:
            sendaddr='amavisNone'
        try:
            if n[1] is not None:
		if len(n) == 2:
		    recvaddr = n[1]
                else:
		    recvaddr = n[1:-1]
        except:
            recvaddr='amavisNone'

    #遍历邮件状态
    for key in sdict:
        statre = re.search(key,m)
        if statre is not None:
            status = sdict[key]
        else:
            pass
    if status == sdict['Blocked SPAM'] or status == sdict['Blocked INFECTED']:
        try:
            filename = filenamere.search(m).group().split(' ')[1]
            #提取mail_id
            try:
                mid = re.search(r'mail_id: [\w\._-]+',m).group().split(' ')[1]
            except:
                mid=''
        except:
	    filename=''
    else:
	filename=''
        try:
            mid = re.search(r'queued_as\: \w{12}',m).group().split(' ')[1]
        except:
            mid=''
    logInfo('info','mail_id:%s FROM:%s MAILTO:%s STATUS:%s filename:%s' % (mid,sendaddr,recvaddr,status,filename))
    sendtime = formatTime(nt)
    recvaddr = sendrecvjoin(recvaddr)
    sendaddr = sendrecvjoin(sendaddr)
    if filename != '':
        sql = "insert into real_mail_log(send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,mail_status,file_name) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (sendtime,mid,sendaddr,recvaddr,ser,sip,status,filename)
    elif filename == '':
        sql = "insert into real_mail_log(send_time,mail_id,send_mail_addr,recv_mail_addr,server_domain,server_ip,mail_status) values('%s','%s','%s','%s','%s','%s','%s')" % (sendtime,mid,sendaddr,recvaddr,ser,sip,status)
    insertMail(sql)


#提取SPF的信息
def getspfInfo(m):
    status = 'spf其它(未知错误)'
    sdict={'action\=PREPEND Received-SPF\: none':'none状态ok',
           'action\=PREPEND Received-SPF\: pass':'pass状态ok',
           'action\=PREPEND Received-SPF\: softfail':'softfail状态拒绝',
           'action\=PREPEND Received-SPF\: neutral':'neutral状态ok',
           'sender policies found':'找到多余的适用发件人策略',
           'Unknown mechanism type':'未知的类型TXT记录',
           'has no applicable sender policy':'spf没有适用的发件人策略',
           'Missing required domain\-spec':'缺少必须的域规范',
	   'Missing required IPv4 address':'缺少必要的IP地址',
           'Junk encountered in record':'垃圾邮件',
           'Junk encountered in mechanism':'垃圾邮件',
           'Maximum void DNS look\-ups limit':'超过最大dns查询限制',
           'Maximum DNS-interactive terms limit':'超过最大dns术语限制',
           'need fully\-qualified hostname':'需要是完全合格域名',
           'blocked using zen\.spamhaus\.org':'邮件地址或ip被加入zen.spamhaus.org黑名单访问https://mxtoolbox.com/domain/',
           'action\=550':'550超时',
           'action\=DUNNO':'DUNNO未知状态'
           }
    m=m.replace('"','')
    mailre = re.compile(r'envelope-from=[^<\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    clientre = re.compile(r'client-ip\=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    serverre = re.compile(r'helo\=(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    timere = re.compile(r'^\w+\s+\d+\s\d{2}\:\d{2}:\d{2}')    
    nt = timere.search(m)
    if nt is not None:
        nt = nt.group()
    try:
        client_ip = clientre.search(m).group().split('=')[1]
    except:
        client_ip = 'spfNone'
    try:
        ser = serverre.search(m).group().split('=')[1]
    except:
        ser = 'spfNone'
    try:
        sendaddr = mailre.search(m).group().split('=')[1]
    except:
        sendaddr = 'spfNone'
    for key in sdict:
        statre = re.search(key,m)
        if statre is not None:
            status = sdict[key]
        else:
            pass
    logInfo('info','Sendmail:%s domain:%s client_ip:%s STATUS:%s' % (sendaddr,ser,client_ip,status))
    sendtime = formatTime(nt)
    sendaddr = sendrecvjoin(sendaddr)
    sql = "insert into real_mail_log(send_time,send_mail_addr,server_domain,client_ip,mail_status) values('%s','%s','%s','%s','%s')" % (sendtime,sendaddr,ser,client_ip,status)
    insertMail(sql)

#提取SPF的信息
def getspfrejectInfo(m):
    status = 'spf其它(未知错误)'
    sdict={'reject\: header Received-SPF\: softfail':'SPF伪装域名或对方TXT记录问题拒绝'
           }

    sendmailre = re.compile(r'from=<[^<\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    tomailre = re.compile(r'to=<[^<\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    helore = re.compile(r'helo\=<(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    timere = re.compile(r'^\w+\s+\d+\s\d{2}\:\d{2}:\d{2}')
    nt = timere.search(m)
    if nt is not None:
        nt = nt.group()
    try:
        sendaddr = sendmailre.search(m).group().split('<')[1]
    except:
        sendaddr = 'spf-reject-None'
    try:
        recvaddr = tomailre.search(m).group().split('<')[1]
    except:
        recvaddr = 'spf-reject-None'
    try:
        ser = helore.search(m).group().split('<')[1]
    except:
	try:
	    ser = sendaddr.split('@')[1]
        except:
	    ser = 'spf-reject-None'
    for key in sdict:
        statre = re.search(key,m)
        if statre is not None:
            status = sdict[key]
        else:
            pass
    logInfo('info','Sendmail:%s MAILTO:%s domain%s STATUS:%s' % (sendaddr,recvaddr,ser,status))
    sendtime = formatTime(nt)
    sendaddr = sendrecvjoin(sendaddr)
    recvaddr = sendrecvjoin(recvaddr)
    sql = "insert into real_mail_log(send_time,send_mail_addr,recv_mail_addr,server_domain,mail_status) values('%s','%s','%s','%s','%s')" % (sendtime,sendaddr,recvaddr,ser,status)
    insertMail(sql)


#提取reject的信息
def getrejectInfo(m):
    status = 'reject其它(未知错误)'
    sdict={'status\=sent':'成功',
'sender policies found':'找到多余的适用发件人策略',
'Unknown mechanism type':'未知的类型TXT记录',
'Missing required IPv4 address':'缺少必要的IP地址',
'has no applicable sender policy':'spf没有适用的发件人策略',
'Missing required domain-spec':'缺少必须的域规范',
'Junk encountered in record':'垃圾邮件',
'Junk encountered in mechanism':'垃圾邮件',
'Maximum void DNS look\-ups limit':'超过最大dns查询限制',
'Maximum DNS-interactive terms limit':'超过最大dns术语限制',
'need fully\-qualified hostname':'需要是完全合格域名',
'blocked using zen\.spamhaus\.org':'邮件地址或ip被加入zen.spamhaus.org黑名单访问https://mxtoolbox.com/domain/',
'Sender address rejected':'发件人地址被拒绝',
'Sender address rejected\: SPF-Result':'对方SPF,txt记录错误',
'Sender address rejected\: Domain not found':'域名未发现',
'Sender address rejected\: User unknown':'用户未知',
'Sender address rejected\: not logged in':'Outlook未勾选smtp需要验证',
'Recipient address rejected\: User unknown in local recipient table':'用户不存在',
'Recipient address rejected':'收人人地址拒绝(需要加白名单)',
'said\: 550 [Mm]ailbox':'收件人未找到(用户可能不存在)',
'said\: 550 Domain frequency limited':'域名发信限制(发邮件太频繁)',
'said\: 55[3-4]':'垃圾邮件',
'[uU]ser not exist':'用户不存在',
'said\: 550 User suspended':'邮箱暂停使用',
'said\: 550 User not found':'用户未找到',
'said\: 550 Mailbox not found':'没有收件箱',
'said\: 451 temporary failure for one or more recipients':'一个或多个收件人临时失败',
'Connection timed out':'连接对方服务器超时',
'lost connection':'与对方失去连接',
'[rR]elay access denied':'中继访问拒绝',           
'Message rejected as spam by Content Filterin':'邮件内容被视为垃圾邮件(加白名单)',
'said\: 550 No [sS]uch [uU]ser':'用户不存在',
'Email address could not be found':'地址不存在',
'does not exist here':'收件人不存在',
'Connection refused':'连接被拒绝',
'said: 422 ERR.LOGIN.USERSTATUS':'错误用户登录状态',
'Please try again later':'请稍后再试',
'said: 501 Bad address syntax':'地址语法错误',
'Undelivered Mail 550 Returned to Sender':'未送达邮件已返回发件人',
'Host not found':'邮件域名未找到',
'INFECTED':'感染病毒',
'Client host rejected':'客户端访问被拒绝',
'No route to host':'没有路由到主机',
'timed out while receiving the initial server greeting':'接收初始服务器问候语时超时',
'Mail content denied':'邮件内容被拒绝',
'Spam message is rejected':'垃圾邮件',
'Recipient not found':'收件人未找到',
'Requested action not taken':'请求未执行',
'Quota exceeded or service disabled':'超出配额或服务禁用',
'Mail is rejected by recipients':'邮件被收件人拒绝',
'relaying denied':'拒绝中继',
'[uU]nknown [Uu]ser':'未知用户',
'[Uu]ser [uU]nknown':'未知用户'}

    sendmailre = re.compile(r'from\=<[\=\+\w\._-]+@+[\=\+\w\._-]+@+[\w\.]+[A-Za-z]+|from\=<[\=\+\w\._-]+@+[\w\.]+[A-Za-z]+')
    tomailre = re.compile(r'to\=<([^<\._-][\w\.-]+@)+(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+')
    serre = re.compile(r'(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[A-Za-z]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    timere = re.compile(r'^\w+\s+\d+\s\d{2}\:\d{2}:\d{2}')
    nt = timere.search(m)
    if nt is not None:
        nt = nt.group()
    try:
        sendaddr = sendmailre.search(m).group().split('<')[1]
    except:
 	    sendaddr = '发件人为空'
    try:
        recvaddr = tomailre.search(m).group().split('<')[1]
    except:
        recvaddr = 'reject-error'
    try:
        ser, sip = serre.search(m).group().split('[')
    except:
        ser = 'reject-error'
        sip = 'reject-error'
    for key in sdict:
        statre = re.search(key,m)
        if statre is not None:
            status = sdict[key]
        else:
            pass
    logInfo('info','Sendmail:%s MAILTO:%s domain:%s IP:%s STATUS:%s' % (sendaddr,recvaddr,ser,sip,status))
    sendtime = formatTime(nt)
    sendaddr = sendrecvjoin(sendaddr)
    recvaddr = sendrecvjoin(recvaddr)
    sql = "insert into real_mail_log(send_time,send_mail_addr,recv_mail_addr,server_domain,server_ip,mail_status) values('%s','%s','%s','%s','%s','%s')" % (sendtime,sendaddr,recvaddr,ser,sip,status)
    insertMail(sql)

#格式化时间用于数据库存储
def formatTime(mtime):
    today = datetime.date.today()
    yer   =     today.strftime("%Y")
    mtime =  yer + mtime
    ntime =  time.strptime(mtime,"%Y%b  %d %H:%M:%S")
    ttime =  time.strftime('%Y-%m-%d %H:%M:%S',ntime)
    return ttime

#MySQL数据插入
def insertMail(sql):
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='mail_report',passwd='mail_report',port=3306,db='mail_report',charset="utf8")
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
	logInfo('info','Insert db is OK')
    except MySQLdb.Error,e:
        logInfo('error',"Mysql Error %d: %s" % (e.args[0],e.args[1]))

#匹配到收件的字段
def matchMailInfo(line):
    m = re.search(r'\w{12}: to=\<[^\._-][\w\.-]+@(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+\>, relay=(local|[Nn]one|(?:[A-Za-z0-9-_]+\.)+[A-Za-z]+\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]:)',line)
    
    if m is not None:
        return True
    else:
	False

#匹配到amavis的字段
def matchamavisInfo(line):
    m = re.search(r'amavis',line)
    m_m = re.search(r'mail_id',line)
    
    if m is not None and m_m is not None:
        return True
    else:
	False

#匹配到SPF的字段
def matchspfInfo(line):
    m = re.search(r'Received-SPF',line)
    
    if m is not None:
        return True
    else:
	False

#匹配到SPF reject的字段
def matchspfrejectInfo(line):
    m = re.search(r'reject\: header Received-SPF\: softfail',line)
    
    if m is not None:
        return True
    else:
	False

#匹配到reject的字段
def matchrejectInfo(line):
    m = re.search(r'reject\: RCPT',line)
    
    if m is not None:
        return True
    else:
	False

#发件人如果是个列表插入数据库会报错，这里将列表值串成一个字符串
def sendrecvjoin(sr):
    if isinstance(sr,list):
	if len(sr) >= 2:
	    srt=sr[0:2]
        srj='-'.join(srt)
	if len(sr) > 2:
	    sr = srj+'...'
        else:
	    sr=srj
    else:
        pass
    return sr

#主程序逻辑
def main(cmdlist):
    running = False
    try:
	while True:
          try:
	    if running == False:
	        p = subprocess.Popen(cmdlist, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		global spid
		spid = p.pid
		running = True
		logInfo('debug','subproc is running, pid is: %s' % str(spid))
	    else:
		pass
            readline = p.stdout.readline()
            if readline == '' and p.poll() != None:
	        running = False
		continue
	    if matchMailInfo(readline):
		getMileInfo(readline)
	    elif matchamavisInfo(readline):
                getamavisInfo(readline)
            elif matchspfrejectInfo(readline):
                getspfrejectInfo(readline)
            elif matchspfInfo(readline):
                getspfInfo(readline)
            elif matchrejectInfo(readline):
                getrejectInfo(readline)
            else:
                pass
          except:
              pass
    except KeyboardInterrupt:
        logInfo('warring','ctrl+d or z')
    except:
	pass

#在Linux中开一个守护进程
def daemon():
    #import daemon
    #from spam import do_main_program

    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent  
            sys.exit(0)
    except OSError, e:
        msg="Error: create the frist sub-process fail, err: %d (%s)" % (e.errno, e.strerror)
        print >>sys.stderr, msg
        sys.exit(4)

    # decouple from parent environment  
    os.chdir("/")
    os.setsid()
    os.umask(022)

    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before  
            sys.exit(0)
    except OSError, e:
        msg="Error: create the second sub-process fail, err: %d (%s)" % (e.errno, e.strerror)
        print >>sys.stdout, msg
        sys.exit(5)

#程序入口
if __name__ == "__main__":
    if len(sys.argv) > 1:
        logfile = sys.argv[1]
        #提取日志的最后每一行
        command = 'tail -n1 -F ' + logfile
        #格式为Linux的shell的格式
        cmdlist = shlex.split(command)
        #开启守护进程
        daemon()
        #检测程序关闭信号
        signal.signal(signal.SIGTERM,subKill)
        #进入主程序
        main(cmdlist)
    else:
        print 'Usage: %s mail.log' % sys.argv[0]

