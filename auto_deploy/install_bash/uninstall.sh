#!/bin/bash

export pack_home='/data/services'
export pack_name=$(basename $1 .tar.gz)

#ֹͣ����
bash $pack_home/$pack_name/admin/stop.sh || exit 1

sleep 2

#���crontab

sed -i "/$pack_name/d" /etc/crontab

#ɾ����Ŀ¼

rm -rf $pack_home/$pack_name

if [ -d $pack_home/$pack_name ] ;then
	echo "rm $pack_name failed"
	exit 1
else
	echo "uninstall $pack_name succeed"
	exit 0
fi

