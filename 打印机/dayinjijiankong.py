import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


phantomjspath='C:\\Python27\\Lib\\site-packages\\phantomjs\\bin\\phantomjs.exe'
zhiurl='http://192.168.241.40/sttray.htm'
mourl='http://192.168.241.40/stsply.htm'

#告警邮件发送
def gaojin(zhimo,n):
    fromuser='yufei.chen@gnetis.com'
    touser='yufei.chen@quanshi.com'
    curtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    subject='192.168.241.40 打印机告警'.decode('utf8')
    if n == 1:
        gjnr='纸盒1剩余纸张:'+str(zhimo[0])+'%'+'\n纸盒2剩余纸张:'+str(zhimo[1])+'%'
        cc=str(gjnr).decode('utf8')
        print cc
    elif n == 2:
        gjnr='墨剩余:'+str(zhimo)+'%'
        cc=str(gjnr).decode('utf8')
        print cc
    #print curtime
    #mailserver='mailcenter.quanshi.com'
    mailserver='192.168.240.216'
    #user='yufei.chen'
    #passwd='awsd=1793.COM'
    user='yufei.chen'
    passwd='awsd=1793.COM'
    #message
    mess=MIMEText(cc,'plain','utf-8')
    mess['From']=Header(fromuser)
    mess['To']=Header(touser)
    mess['Subject']=Header(subject)
    mess['Date']=Header(curtime)

    #login auth
    smtpa=smtplib.SMTP(mailserver)
    smtpa.login(user,passwd)

    #send mail
    smtpa.sendmail(fromuser,touser,mess.as_string())
    print 'success'

#正则处理，返回数值
def rex(htmltag):
    a=re.compile(r'>(.*)%<')
    b=re.search(a,str(htmltag))
    c=b.group(1)
#    print c
    return c
#htm的URL使用js执行，安装了包phantomjs
def jsexec(hurl,panduan):
   dirver=webdriver.PhantomJS(executable_path=phantomjspath)
   #time.sleep(1)
   dirver.get(hurl)
   data=dirver.page_source
   html=BeautifulSoup(data,"html.parser")
 #  print html
   if panduan == 1:
       zhity=[]
       zhity.append(rex(html.find_all('small')[9]))
       zhity.append(rex(html.find_all('small')[16]))
#       print zhity
       if zhity <= 5:
          gaojin(zhity,1)
   elif panduan == 2:
       mo=(rex(html.find_all('small')[5]))
  #     print mo
       if mo <= 5:
          gaojin(mo,2)

jsexec(zhiurl,1)
jsexec(mourl,2)
