#!/bin/bash

bash_home="/data/install_bash"

#��ж��
bash $bash_home/uninstall.sh $1 || exit 1

#�ٰ�װ
bash $bash_home/install.sh $2 $3 || exit 1


