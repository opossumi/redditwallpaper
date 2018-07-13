#!/bin/bash
seconds=$(( ( RANDOM % 3000 )  + 1 ))
echo "Sleeping $seconds seconds"
sleep $seconds
/usr/local/bin/redditwallpaper "$@"
