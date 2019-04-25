#!/bin/bash
#svn版本导入
awk '{
if(($2+1) <= $3){
cmd="svnadmin load /home/svn/";
cmdf="<";
svnl="/root/svnloadscp/"
svnsd=$2+1"-"$3;
system(cmd$1 cmdf svnl $1svnsd)
}
}' verupdate.txt
sleep 2
rm /root/svnloadscp/*