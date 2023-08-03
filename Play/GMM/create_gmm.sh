#!/bin/bash

#s is threshold
#a is voxel size

mapname=$1
threshold=$2

for i in 5 20 25 30 50 #number of Gaussians
do

python /usr/lib/python3.6/dist-packages/IMP/isd/create_gmm.py $mapname $i $mapname.gmm.$i.txt -s $threshold -m $mapname.gmm.$i.mrc -a 2.0 -i 10000000

done

