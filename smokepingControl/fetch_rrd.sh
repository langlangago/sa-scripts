#!/bin/bash
#rrdtool fetch /var/lib/smokeping/telcom/beijingyangqiaoshuangxian-02-118.rrd AVERAGE --start now-4hours > /home/langxiaowei/test
#/20 20 is icmp counts

sed -i '1,2 d ' '/home/langxiaowei/test'


test_rows=`wc -l '/home/langxiaowei/test'|awk '{print$1}'`
sed -i "${test_rows} d " '/home/langxiaowei/test'


awk '{print $4}' '/home/langxiaowei/test' >'/home/langxiaowei/test4'
sed -i '/\-nan/ d' '/home/langxiaowei/test4'
me_av=`wc -l '/home/langxiaowei/test4'|awk '{print$1}'`
if [ $me_av -eq 0 ];
then
       echo -e "median rtt \t: -nan s avg\t -nan s max\t"
else
       for i in `cat /home/langxiaowei/test4`
       do
                echo $i | awk '{printf("%.5f\n",$0)}' >> '/home/langxiaowei/nums2'
       done
       avg_med=`awk '{b+=$1} END{print b}' '/home/langxiaowei/nums2'`
       max_med=`awk '{if ($1>b) b=$1} END{print b}' '/home/langxiaowei/nums2'`
       result_med=`echo ${avg_med}|awk '{printf ("%.1fms",$0/'"${me_av}"'*1000)}'`
       resul_max_med=`echo ${max_med}|awk '{printf ("%.1fms",$0*1000)}'`
       rm -f '/home/langxiaowei/nums2'
       echo -e "median rtt \t: $result_med  avg\t $resul_max_med  max\t"

fi
awk '{print $3}' '/home/langxiaowei/test' >'/home/langxiaowei/test3'
sed -i '/\-nan/ d' '/home/langxiaowei/test3'
me_av=`wc -l '/home/langxiaowei/test3'|awk '{print$1}'`
for i in `cat /home/langxiaowei/test3`
do
       echo $i | awk '{printf("%.5f\n",$0)}' >> '/home/langxiaowei/nums'


done
avg_los=`awk '{b+=$1} END{print b}'  '/home/langxiaowei/nums'`
max_los=`awk '{if ($1>a) a=$1} END{print a}' '/home/langxiaowei/nums'`
result_loss=`echo ${avg_los}|awk '{printf("%.2f %",$0/'"${me_av}"'/20*100)}'`
result_max_loss=`echo ${max_los}|awk '{printf("%.2f %",$0/20*100)}'`
rm -f '/home/langxiaowei/nums'
echo -e "packet loss \t: $result_loss  avg\t $result_max_loss  max\t"
