#!/bin/bash
fname=$(ls -t ~/.wallpapers|head -n100|sort -R|head -n1)
fpath="$HOME/.wallpapers/$fname"
/usr/bin/feh --bg-scale "$fpath"
