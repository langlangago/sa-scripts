#!/bin/bash


function install(){

user=`whoami`

for ip in $(cat $1)
do
	scp -P 32200 $2 $user@$ip:/home/$user/
	if [ $? -ne 0 ] ; then 
		echo "Scp $ip error"
		exit 1
	fi
	ssh $ip "sudo cp /home/$user/$2 /data/backup && rm -rf /home/$user/$2"
    ssh $ip "sudo /data/install_bash/install.sh $2 $3;echo $?" 
    if [ $? -ne 0 ] ; then
		echo "Start $ip error"
	else
		echo "Start $ip Done\n"
	fi
	sleep 5
done
}


function start(){

pack_name=$(basename $2 .tar.gz)

for ip in $(cat $1)
do
	ssh $ip "sudo /data/services/$pack_name/admin/start.sh"
	sleep 5
done
}


function stop(){

pack_name=$(basename $2 .tar.gz)

for ip in $(cat $1)
do
	ssh $ip "sudo /data/services/$pack_name/admin/stop.sh"
	sleep 5
done
}


function restart(){

pack_name=$(basename $2 .tar.gz)

for ip in $(cat $1)
do
	ssh $ip "sudo /data/services/$pack_name/admin/restart.sh"
	sleep 5
done
}


function uninstall(){

pack_name=$(basename $2 .tar.gz)

for ip in $(cat $1)
do
	ssh $ip "sudo /data/install_bash/uninstall.sh $pack_name"
	sleep 5
done
}


function update(){

user=`whoami`
old_pack=$(basename $2 .tar.gz)
new_pack=$(basename $3 .tar.gz)

for ip in $(cat $1)
do
	scp -P 32200 $3 $user@$ip:/home/$user
	if [ $? -ne 0 ]; then
		echo "scp $ip error"
		exit 1
	fi
	ssh $ip "sudo cp /home/$user/$3 /data/backup && rm -rf /home/$user/$3" || exit 1
	ssh $ip "sudo /data/install_bash/update.sh $old_pack $new_pack $4" || exit 1
	sleep 5
done
}


function rollback(){

new_pack=$(basename $2 .tar.gz)
old_pack=$(basename $3 .tar.gz)

for ip in $(cat $1)
do
	ssh $ip "sudo /data/install_bash/update.sh $new_pack $old_pack $4" 
	sleep 5
done
}

function help(){

echo ""
echo "Usage:"
echo ""
echo "./auto_deploy.sh	install 	hosts.txt	 pack_name.tar.gz	 process_count(default=1)"
echo ""
echo "./auto_deploy.sh 	start		hosts.txt	 pack_name.tar.gz "
echo ""
echo "./auto_deploy.sh 	stop 		hosts.txt	 pack_name.tar.gz"
echo ""
echo "./auto_deploy.sh 	restart 	hosts.txt	 pack_name.tar.gz"
echo ""
echo "./auto_deploy.sh 	uninstall 	hosts.txt	 pack_name.tar.gz"
echo ""
echo "./auto_deploy.sh 	update		hosts.txt	 old_pack_name.tar.gz	 new_pack_name.tar.gz	process_count(default=1)"
echo ""
echo "./auto_deploy.sh 	rollback 	hosts.txt	 new_pack_name.tar.gz	 old_pack_name.tar.gz	process_count(default=1)"
echo ""

}

if [ "$1" = "help" ]; then
	help
elif [ "$1" = "install" ]; then
	install $2 $3 $4
elif [ "$1" = "start" ]; then
	start $2 $3
elif [ "$1" = "stop" ]; then
	stop $2 $3
elif [ "$1" = "restart" ]; then
	restart $2 $3
elif [ "$1" = "uninstall" ]; then
	uninstall $2 $3
elif [ "$1" = "update" ]; then
	update $2 $3 $4 $5
elif [ "$1" = "rollback" ]; then
	rollback $2 $3 $4 $5
else 
	help
fi
