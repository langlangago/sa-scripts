#!/bin/bash

agent_home="/data/services"
my_home="/home/langxiaowei"

if [ -d $agent_home/falcon-agent ];then
	echo "Agent was already here!!!"
	exit 1
fi 

scp -P 32200 langxiaowei@11.11.11.1:$my_home/auto_agent/falcon-agent.tar.gz $my_home || exit 1

sudo mv $my_home/falcon-agent.tar.gz  $agent_home 

sudo tar -zxf $agent_home/falcon-agent.tar.gz -C $agent_home && sudo rm -rf $agent_home/falcon-agent.tar.gz || exit 1

sudo sed -i "s#\"hostname\": \"\",#\"hostname\": \"$1 $2\",#g" $agent_home/falcon-agent/cfg.json || exit 1
sudo sed -i "s#\"ip\": \"\",#\"ip\": \"$2\",#g" $agent_home/falcon-agent/cfg.json || exit 1

sudo $agent_home/falcon-agent/control start || exit 1

sudo $agent_home/falcon-agent/control status 
