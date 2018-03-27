#!/bin/bash

fnames=`ls *.dos`
for fname in $fnames; do
	v="python -c "'$fname'.split()""
	echo "$v"
done
