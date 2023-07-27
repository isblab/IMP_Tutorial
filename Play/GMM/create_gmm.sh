#!/bin/bash

#s is threshold
#a is voxel size

mapname=$1
threshold=$2

for i in 5 10 20  #number of Gaussians
do

python ~/imp-clean/imp/modules/isd/pyext/src/create_gmm.py $mapname $i $mapname.gmm.$i.txt -s $threshold -m $mapname.gmm.$i.mrc -a 2.0 -i 10000000

done

