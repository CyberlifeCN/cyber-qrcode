#!/bin/bash

cd $(dirname $0)

IP_LIST=${IP_LIST:-127.0.0.1}

if [ -z "$IP_LIST" ]; then
	echo "environment var 'IP_LIST' is empty"
	exit 1
fi

case "$1" in
	-h)
		echo "Usage: IP_LIST='IP-1 IP-2...' $0 [-h/--prepare]"
		exit 0
		;;
	--prepare)
		for ip in $IP_LIST
		do
			ssh-copy-id -i $HOME/.ssh/id_rsa.pub root@$ip && echo "$ip run ssh-copy-id success" || echo "$ip run ssh-copy-id failed"
		done
		exit 0
		;;
esac

file="$(./1-rpmbuild.sh)"
dir="$HOME/rpmbuild/RPMS/x86_64"

for ip in $IP_LIST
do
	scp $dir/$file root@${ip}:/tmp &&
	ssh root@${ip} "systemctl stop cyber-qrcode; rpm -Uvh --replacepkgs --force /tmp/$file && rm -f /tmp/$file && echo success" || { echo "$ip failed" ; continue; }

	for svc in qrcode qrcode.swagger
	do
		ssh root@${ip} "systemctl enable cyber-$svc && systemctl start cyber-$svc"
	done

	echo "$ip done"
done

echo "-------------------------------------------------------------"
{
	echo "IP $file"

	for ip in $IP_LIST
	do
		status=$(ssh root@${ip} "rpm -q cyber-qrcode")
		echo "$ip $status"
	done
} | column -t

read -n 1 -p "Press any key to show cyber-status..."
clear

for ip in $IP_LIST
do
	echo "$ip: cyber-status"
	echo
	ssh root@${ip} "/usr/local/bin/cyber-status"
	echo
	echo "$ip: cyber-status"
	echo
	read -n 1 -p "Press any key to show next cyber-status..."
	clear
done
