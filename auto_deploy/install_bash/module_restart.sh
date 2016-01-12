

#先停进程

bash $install_path/admin/stop.sh || exit 1

sleep 5

#再起进程

bash $install_path/admin/start.sh || exit 1


