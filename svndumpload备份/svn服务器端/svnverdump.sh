#!/bin/bash
#svn版本导出
if [ ! -d "/root/svndumpscp" ];then
  mkdir /root/svndumpscp
fi
awk '{
if(($2+1) <= $3){
cmd="svnadmin dump -r ";
ver=$2+1":"$3
canshu=" --incremental "
filedir="/home/svn/";
dumpdir="/root/svndumpscp/"
cmdf=">";
svnsd=$2+1"-"$3;
system(cmd ver canshu filedir$1 cmdf dumpdir$1svnsd)
}
}' verupdate.txt
scp /root/svndumpscp/* root@192.168.240.201:/root/svnloadscp/
sleep 2
rm /root/svndumpscp/*