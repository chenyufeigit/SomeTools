#!/bin/bash
#将svn的.bak文件导入到库，库名是从后面文件中读取的库名作为$1
awk '{cmd="svnadmin load /home/svn/";cmdf="<";cmdv=".bak";system(cmd $1 cmdf $1cmdv)}' ../k
