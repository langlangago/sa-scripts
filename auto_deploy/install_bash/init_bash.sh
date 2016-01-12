#!/bin/bash

cat >> $pack_home/$pack_name/admin/monitor.sh << EOF
#!/bin/bash

source $pack_home/$pack_name/admin/common-var.conf

EOF
cat $bash_home/module_monitor.sh >> $pack_home/$pack_name/admin/monitor.sh
chmod 755 $pack_home/$pack_name/admin/monitor.sh

cat >> $pack_home/$pack_name/admin/start.sh << EOF
#!/bin/bash

source $pack_home/$pack_name/admin/common-var.conf

EOF
cat $bash_home/module_start.sh >> $pack_home/$pack_name/admin/start.sh
chmod 755 $pack_home/$pack_name/admin/start.sh

cat >> $pack_home/$pack_name/admin/stop.sh << EOF
#!/bin/bash

source $pack_home/$pack_name/admin/common-var.conf

EOF
cat $bash_home/module_stop.sh >> $pack_home/$pack_name/admin/stop.sh
chmod 755 $pack_home/$pack_name/admin/stop.sh

cat >> $pack_home/$pack_name/admin/restart.sh << EOF
#!/bin/bash

source $pack_home/$pack_name/admin/common-var.conf

EOF
cat $bash_home/module_restart.sh >> $pack_home/$pack_name/admin/restart.sh
chmod 755 $pack_home/$pack_name/admin/restart.sh
