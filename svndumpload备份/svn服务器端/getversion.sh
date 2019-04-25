#!/bin/bash
awk '{printf "%s\t",$1;cmd="svnlook youngest /home/svn/"$1;system(cmd)}' svnlist.txt > ver240.201.txt
scp /root/script/svnbakjb/ver11.216.txt root@192.168.240.201:/root/script/