#!/bin/bash

for n in '1' '2' '3' '4' '5' '6' '7' '8' '9' '10'
do
	for m in '1' '2' '3' '4' '5' '6' '7' '8' '9' '10'
	do
  		python ./core.py -n$n -m$m; 
	done
done