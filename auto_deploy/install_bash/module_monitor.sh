
#log

flag=$(cat $install_path/admin/auto_start.flag)

if [ "$flag" = 1 ]; then
	exit 0
fi

pids=$(pidof $pname)

num=$(echo $pids|wc -w)


if [ $num -lt $count ] ; then
	echo "$(date '+%F %T')|current $pname num = $num [< $count], pid=[$pids]"
	#ps -lf $pids
	python $bash_home/alarm.py $install_path/bin/$pname:\($num\<$count\) $pname || exit 1
	bash $install_path/admin/start.sh || exit 1
	exit $?
else
	echo "current num of $pname=$num,pids=[$pids]"
	ps -lf $pids
	exit 0
fi
