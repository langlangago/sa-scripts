$!/bin/bash

bash_home="/data/install_bash"

#��ж���°汾
bash $bash_home/uninstall.sh $1 || exit 1

#�ٰ�װ�ɰ汾
bash $bash_home/install.sh $2 $3 || exit 1
