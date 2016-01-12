#!/bin/bash

echo "#online log" >> /etc/crontab
echo "0 0 * * * root /data/sh/backup_online_log.sh > /data/sh/backup.log 2>&1" >> /etc/crontab
