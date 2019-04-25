import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

#config
fromuser='yufei.chen@quanshi.com'
#touser='test2@mailtest.com'
#fromuser='yufei.chen@gnetis.com'
#touser='895605789@qq.com'
touser='yufei.chen@quanshi.com'
subject='python test'


#mailserver='mailcenter.quanshi.com'
mailserver='192.168.240.214'
#user='yufei.chen'
#passwd='a'
user='yufei.chen@quanshi.com'
passwd='awsd=1793.COM'
text='python mail send test'
def sendmailstart(mailserver,fromuser,touser,subject,user,passwd):
    #message
    curtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(curtime)
    mess=MIMEText(text,'plain','utf-8')
    mess['From']=Header(fromuser)
    mess['To']=Header(touser)
    mess['Subject']=Header(subject)
    mess['Date']=Header(curtime)
    try:
        #login auth
        smtpa=smtplib.SMTP(mailserver)
        smtpa.login(user,passwd)

        #send mail
        smtpa.sendmail(fromuser,touser,mess.as_string())
        print("Send Success!")

    except Exception as e:
        print("Send Failed!")
        print("because:%s" %e)

for i in range(1):
    sendmailstart(mailserver,fromuser,touser,subject,user,passwd)


















