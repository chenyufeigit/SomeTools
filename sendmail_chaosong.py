import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

#config
fromuser='yufei.chen@quanshi.com'
#touser='test2@mailtest.com'
#fromuser='yufei.chen@gnetis.com'
#touser='895605789@qq.com'
touser=['chenyiying93@mailtest.com']
subject='python test'
ccto_list=['test1@mailtest.com']
bccto_list=['test2@mailtest.com']

#mailserver='mailcenter.quanshi.com'
mailserver='192.168.21.226'
#user='yufei.chen'
#passwd='a'
user='yufei.chen@quanshi.com'
passwd='q111111'
text='python mail send test'
def sendmailstart(mailserver,fromuser,touser,subject,user,passwd):
    #message
    curtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(curtime)
    mess=MIMEText(text,'plain','utf-8')
    mess['From']=Header(fromuser)
    mess['To']=','.join(touser)
    mess['cc']=','.join(ccto_list)
    mess['Subject']=Header(subject)
    receive = touser
    receive.extend(ccto_list)
    receive.extend(bccto_list)
    mess['Date']=Header(curtime)
    try:
        #login auth
        smtpa=smtplib.SMTP(mailserver)
        smtpa.login(user,passwd)

        #send mail
        smtpa.sendmail(fromuser,receive,mess.as_string())
        print("Send Success!")

    except Exception as e:
        print("Send Failed!")
        print("because:%s" %e)

for i in range(1):
    sendmailstart(mailserver,fromuser,touser,subject,user,passwd)


















