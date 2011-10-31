#!/bin/bash
user=$1
host=$2
rdir=$3
ldir=$4
if [ "$#" -lt 4 -o "$#" -gt 4  ]; then
    echo "Usage ./sshmount username hostname remotedir localdir"
    echo "Remotedir -> Remote directory to be mounted"
    echo "Localdir -> Local path where to mount"
    exit 1;
else
    /usr/bin/sshfs $user@$host:$rdir $ldir -oauto_cache,reconnect,volname=$host
fi
