# -*- coding: cp936 -*-  
''''' 
����һ��python server������ָ���˿ڣ� 
����ö˿ڱ�Զ�����ӷ��ʣ����ȡԶ�����ӣ�Ȼ��������ݣ� 
����������Ӧ������ 
'''  
if __name__=="__main__":  
    import socket    
    print "Server is starting"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    sock.bind(('localhost', 4000))  #����soket����IP��ַ�Ͷ˿ں�  
    sock.listen(5) #������������������������Ӻ�server��ͨ����ѭFIFOԭ��  
    print "Server is listenting port 4000, with max connection 5"   
    while True:  #ѭ����ѯsocket״̬���ȴ�����  
                  
        connection,address = sock.accept()    
        try:    
            connection.settimeout(50)  
                        #���һ�����ӣ�Ȼ��ʼѭ������������ӷ��͵���Ϣ  
            while True:  
                    buf = connection.recv(819200)    
                    print "Get value " +buf  
                    if  buf!='0':    
                        connection.send('please go out!')   
                        print "send refuse"  
                    else:   
                        print "close"  
                        break  #�˳����Ӽ���ѭ��  
        except socket.timeout:  #����������Ӻ󣬸��������趨��ʱ���������ݷ�������time out  
            print 'time out'
            print "closing one connection" #��һ�����Ӽ���ѭ���˳������ӿ��Թص�  
            connection.close()
