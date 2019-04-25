awk '{cmd="svnadmin dump /home/svn/";cmdf=">";cmdv=".bak";system(cmd $1 cmdf $1cmdv)}' ../k
