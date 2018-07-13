#!/bin/bash
fname=$(ls -t ~/.wallpapers|head -n100|sort -R|head -n1)
path="$HOME/.wallpapers/$fname"
/usr/bin/feh --bg-scale $path
