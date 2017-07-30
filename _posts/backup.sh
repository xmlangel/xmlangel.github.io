#!/bin/sh

DIRS=`ls -l $PWD | egrep '^d' | awk '{print $9}'`

# "ls -l $MYDIR"      = get a directory listing
# "| egrep '^d'"           = pipe to egrep and select on ly the directories
# "awk '{print $9}'" = pipe the result from egrep to awk and print on ly the 9th field

for DIR in $DIRS
do
    echo ${DIR}
    tar -czvf - ${DIR}|pv -L 1m>${DIR}.tar.gz
    aws s3 cp ${DIR}.tar.gz s3://whatap-yard-backup/yard/${DIR}.tar.gz
      #rm -rf ${DIR}
done