#!/bin/bash

bash_home="/data/install_bash"

#先卸载
bash $bash_home/uninstall.sh $1 || exit 1

#再安装
bash $bash_home/install.sh $2 $3 || exit 1


