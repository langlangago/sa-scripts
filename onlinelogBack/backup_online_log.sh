#!/bin/bash

backup="/data/online_log_backup"
log="/data/yy/log/nmob_online_d"

yesterday=`date +%s -d "-1 day"`
now=`date +%s`
day=`date +%F -d "-1 day"`
old_day=`date +%F -d "-6 day"`

#backup yesterday logs

if [ ! -d $backup/$day ];then
	mkdir -p $backup/$day
else
	echo "..............."
fi


for file in `ls $log`
do
	mtime=`stat -c %Y $log/$file`
	hour=`stat -c %y $log/$file | awk '{print $2}' |cut -b 1-5`

	if [ $mtime -gt $yesterday -a $mtime -lt $now ] ;then
		cp $log/$file $backup/$day/nmob_online_d.log.$hour.gz
		if [ $? -ne 0 ];then
			echo "cp $log/$file failed!"
			exit 1
		fi

	fi
	sleep 1
done

echo "all file backup success!"

#delete 5 days ago logs

if [ -d $backup/$old_day ];then
	rm -rf $backup/$old_day
else
	echo "5 days ago log is not exits!"
fi


