#!/bin/bash
# 将11.216传过来的svn库和240.201的库版本做对比,如有不同将会显示版本库及两方的版本，bak的版本不可能比线上的版本低
awk '{
  if(FNR==NR){
    a[FNR]=$2
  }
  if(FNR<NR){
    if(a[FNR]<$2){
      print $1,a[FNR],$2
    }
  }
}' ver240.201.txt ver11.216.txt | awk '{print $1,$2,$3}' > verupdate.txt
if [ ! -d "/root/svndumpscp" ];then
  mkdir /root/svndumpscp
fi
sleep 2
scp /root/script/verupdate.txt root@192.168.11.216:/root/script/svnbakjb/
