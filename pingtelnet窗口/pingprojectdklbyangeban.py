from PyQt5 import QtWidgets, QtGui
import sys
import os
from form import Ui_Form    # 导入生成form.py里生成的类
import telnetlib
import re
import subprocess



# 方案2:不同主机端口不同
hostport=[
"54.222.216.166", "80", "54.222.216.166", "443",
"52.80.112.76", "80", "52.80.112.76", "443",
"52.80.87.134", "80", "52.80.87.134", "443",
"54.223.238.83", "80", "54.223.238.83", "443",
"54.223.226.22", "80", "54.223.226.22", "443",
"54.223.250.228", "80", "54.223.250.228", "443",
"aws-beea-cas-out-1954274744.cn-north-1.elb.amazonaws.com.cn", "80", "aws-beea-cas-out-1954274744.cn-north-1.elb.amazonaws.com.cn", "443",
"203.174.112.252", "80", "203.174.112.252", "443",
"203.174.112.253", "80", "203.174.112.253", "443",
"203.174.105.200", "80", "203.174.105.200", "443",
"203.174.105.201", "80", "203.174.105.201", "443",
"203.174.105.202", "80", "203.174.105.202", "443",
"203.174.105.203", "80", "203.174.105.203", "443",
"aws-beea-workspace-nginx-233353822.cn-north-1.elb.amazonaws.com.cn", "80", "aws-beea-workspace-nginx-233353822.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-nginx-257170742.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-nginx-257170742.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-BeeA-nginxweb-1554707740.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-BeeA-nginxweb-1554707740.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-BeeA-quanshisetup-1393757798.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-BeeA-quanshisetup-1393757798.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-fs-nginx-out-1141631578.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-fs-nginx-out-1141631578.cn-north-1.elb.amazonaws.com.cn", "443",
"AWS-beeA-ucase-out-1719871851.cn-north-1.elb.amazonaws.com.cn", "80", "AWS-beeA-ucase-out-1719871851.cn-north-1.elb.amazonaws.com.cn", "443",


]
yestelnet=[]
yeshost=[]
notelnet=[]
nohost=[]

# telnet实现返回notelnet列表包含telnet不通的主机IP和端口
# 方案2:
def t(self,hostport):
    yestelnet=[]
    notelnet=[]
    cs="测试中"
    # 循环主机和端口
    lang=len(hostport)
    for r in range(0, lang, 2):
        i=hostport[r]
        p=hostport[r+1]
        cs=cs+'.'
        self.text_2.setText(cs)
        QtWidgets.QApplication.processEvents()
        try:
            tn = telnetlib.Telnet(i,p,1)
            yestelnet.append(str(i)+str(p))
        except:               
            notelnet.append(str(i)+":"+str(p))
    if notelnet == []:
        notelnet=['端口全部正常,OK!']
    self.text_2.clear()
    self.text_2.append("测试完成!")
    QtWidgets.QApplication.processEvents()
    return notelnet

def p(self,hostport):
    yeshost=[]
    nohost=[]
    cs="测试中"
    lang=len(hostport)
    for r in range(0,lang,4):
        a=0
        i=hostport[r]
        cs=cs+'.'
        self.text_1.setText(cs)
        QtWidgets.QApplication.processEvents()
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
    self.text_1.clear()
    self.text_1.append("测试完成!")
    QtWidgets.QApplication.processEvents()
    return nohost




class mywindow(QtWidgets.QWidget,Ui_Form):    
    def __init__(self):    
        super(mywindow,self).__init__()    
        self.setupUi(self)
        
    def cleantext(self):
        yestelnet=[]
        yeshost=[]
        notelnet=[]
        nohost=[]
        self.text_1.clear()
        self.text_2.clear()

    #定义槽函数
    def telnetping(self):
        yestelnet=[]
        yeshost=[]
        notelnet=[]
        nohost=[]
        QtWidgets.QApplication.processEvents()
        
        notelnet=t(self,hostport)
        nohost=p(self,hostport)
        for i in notelnet:
            self.text_2.append(str(i))
        for i in nohost:
            self.text_1.append(str(i))



        #定义槽函数
    def telnetonly(self):
        yestelnet=[]
        yeshost=[]
        notelnet=[]
        nohost=[]
        QtWidgets.QApplication.processEvents()
        notelnet=t(self,hostport)
        for i in notelnet:
            self.text_2.append(str(i))


        #定义槽函数
    def pingonly(self):
        yestelnet=[]
        yeshost=[]
        notelnet=[]
        nohost=[]
        QtWidgets.QApplication.processEvents()
        nohost=p(self,hostport)
        for i in nohost:
            self.text_1.append(str(i))
        




app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.show()
sys.exit(app.exec_())
