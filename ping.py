import os
ipduan='192.168.241.'

for ip in range(100,255):
    ip=str(ip)
    ipduan=str(ipduan)
    a=os.popen("ping -n 1 -w 10 %s%s"%(ipduan,ip))
    result=a.readlines()[2]
    #if result != '\xc7\xeb\xc7\xf3\xb3\xac\xca\xb1\xa1\xa3\n': #这些字符是"请求超时。"
    #    result=list(result)                 #此处三行是去掉结果里面的\n换行符
    #    result=result[0:len(result)-1]
    #    result=''.join(result)
    #    print ipduan+ip+"\t"+result
    print(ipduan+ip+"\t"+result)



#host=['192.168.12.89','192.168.12.253']
#port=['3389','80']

#yestelnet=[]
#yeshost=[]
#notelnet=[]
#nohost=[]

#def tp(host,port):
#    for i in host:
#        for p in port:
#            try:
#                tn = telnetlib.Telnet(i,p,2)
#                #return "主机:"+str(i)+"\t端口:"+str(p)+"  \tOK\n"
#                yestelnet.append(str(i)+str(p))
#            except:
#                a=os.popen("ping -n 1 -w 90 %s" %i)
#                b=a.readlines()
#                #return "主机:"+str(i)+"\t端口:"+str(p)+"  \t不通"+b[2]+i
#                notelnet.append(str(i)+":"+str(p))
#                nohost.append(b)
#                #print(b)
#    return notelnet,nohost

#notelnet,nohost=tp(host,port)
#for i in nohost:
#    print(i[2])
#print(nohost[0][2])

import telnetlib
host=[]
for ip in range(1,250):
    ip=str(ip)
    ipduan=str(ipduan)
    host.append(ipduan+ip)

port=['22']
for i in host:
    for p in port:
        try:
            tn = telnetlib.Telnet(i,p,2)
            print("主机:"+str(i)+"\t端口:"+str(p)+"  \tOK\n")
        except:
            #print("主机:"+str(i)+"\t端口:"+str(p)+"  \t不通")
            #a=os.popen("ping -n 1 -w 90 %s" %i)
            #b=a.readlines()
            #print(b[2],i)
            pass
    

ipduan=[
'223.6.250.177',
'121.199.251.159',
'121.43.79.9',
'112.124.22.124',
'114.215.192.218',
'120.26.100.137',
'120.55.105.204',
'120.55.249.238',
'120.27.129.71',
'42.120.43.142',
'42.120.43.143',
'218.244.150.169',
'114.55.59.45',
'42.121.122.156',
'42.120.60.94',
]
for ip in ipduan:
    ip=str(ip)
    a=os.popen("ping -n 1 -w 10 %s"%ip)
    result=a.readlines()[2]
    if result != '\xc7\xeb\xc7\xf3\xb3\xac\xca\xb1\xa1\xa3\n': #这些字符是"请求超时。"
        result=list(result)                 #此处三行是去掉结果里面的\n换行符
        result=result[0:len(result)-1]
        result=''.join(result)
        print(ip)
        #print ip+"\t"+result
    #print ip+"\t"+result

