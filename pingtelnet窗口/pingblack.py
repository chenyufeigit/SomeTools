import sys
import os
import telnetlib
import re
import subprocess



# 方案2:不同主机端口不同
hostport=[
"AWS-beeA-nginx-257170742.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-nginx-257170742.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-cas-out-1954274744.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-cas-out-1954274744.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-BeeA-nginxweb-1554707740.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-BeeA-nginxweb-1554707740.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-BeeA-quanshisetup-1393757798.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-BeeA-quanshisetup-1393757798.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-fs-nginx-out-1141631578.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-fs-nginx-out-1141631578.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-ucase-out-1719871851.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-ucase-out-1719871851.cn-north-1.elb.amazonaws.com.cn", "443",
"cme-coreproxy-2020165351.cn-north-1.elb.amazonaws.com.cn", "80", "cme-coreproxy-2020165351.cn-north-1.elb.amazonaws.com.cn", "443",
"cme-joinmeeting-182987973.cn-north-1.elb.amazonaws.com.cn", "80", "cme-joinmeeting-182987973.cn-north-1.elb.amazonaws.com.cn", "443",
"cme-liveserver-90944093.cn-north-1.elb.amazonaws.com.cn", "80", "cme-liveserver-90944093.cn-north-1.elb.amazonaws.com.cn", "443",
"cme-openapi-235933215.cn-north-1.elb.amazonaws.com.cn", "80", "cme-openapi-235933215.cn-north-1.elb.amazonaws.com.cn", "443",
"cme-uniform-305779138.cn-north-1.elb.amazonaws.com.cn", "80", "cme-uniform-305779138.cn-north-1.elb.amazonaws.com.cn", "443",

]
yestelnet=[]
yeshost=[]
notelnet=[]
nohost=[]

# telnet实现返回notelnet列表包含telnet不通的主机IP和端口
# 方案2:
def t(hostport):
    yestelnet=[]
    notelnet=[]
    cs="测试中"
    # 循环主机和端口
    lang=len(hostport)
    for r in range(0, lang, 2):
        i=hostport[r]
        p=hostport[r+1]
        cs=cs+'.'
        try:
            tn = telnetlib.Telnet(i,p,1)
            yestelnet.append(str(i)+str(p))
        except:               
            notelnet.append(str(i)+":"+str(p))
    if notelnet == []:
        notelnet=['端口全部正常,OK!']
    return notelnet

def p(hostport):
    yeshost=[]
    nohost=[]
    cs="测试中"
    lang=len(hostport)
    for r in range(0,lang,4):
        a=0
        i=hostport[r]
        cs=cs+'.'
        loop="ping -n 2 -w 100 %s" %i
        a=subprocess.call(loop,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        print(a)
        print(i)
        if a == 1:
            a=subprocess.Popen(loop,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            a.stdout.readline()
            a.stdout.readline()
            c=a.stdout.readline()
            c=c.decode('gbk')
            c=re.sub(r'\r\n','',c)
            nohost.append(i+"       \t"+c)
    if nohost == []:
        nohost =  ["IP全部正常,OK!"]
    return nohost
t(hostport)
p(hostport)
input("please input anykey end!:")
