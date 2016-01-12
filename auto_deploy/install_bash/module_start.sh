#日志文件

log=$pack_home/$pack_name/admin/start.log

#进程数检查
x=$(pidof $pname|wc -w)
y=$((count-x))
echo "delta=$y"


#进程数等于$count就退出


if [ $y -le 0 ] ; then
	pidof $pname | xargs -r ps -lf
	echo "$pname num ($x) >= $count , no need to start , quit"
	exit 0
fi

#启动进程

cd $pack_home/$pack_name/bin || exit 1

for ((i=1;i<=$y;i++)); do
	echo "start #$i"
	nohup ./$pname >> $log 2>&1 &
	sleep 2
done

#二次确认

if [ $(pidof $pname|wc -w) -eq $count ] ; then
	echo "Start $pname OK"
	echo "0" > $pack_home/$pack_name/admin/auto_start.flag
	exit 0
else
	echo "Start $pname Fail"
	exit 1
fi
