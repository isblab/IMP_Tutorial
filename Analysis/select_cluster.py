###################################################
######## Select Cluster and Extract models ########
###################################################

# Imports
import numpy as np
import sys
import os

def return_Max_cluster():
	file = sys.argv[1]                  #Input the summary_hdbscan_clustering.dat file

	with open (file, "r") as f:
		cluster_summary = f.readlines()

	models_count = {}
	#Get the index for the N_models header
	index = cluster_summary[0].split(",").index("N_models") 

	#Remove the unclustered models entry
	cluster_summary.remove(cluster_summary[0][:])

	#Find the cluster with maximum no. of models
	for i in range(len(cluster_summary)):
		line = cluster_summary[i].split(",")
		if line[0] != "-1":
			models_count[int(line[0])] = int(line[index])
		else:
			continue                              #"Jaisa chal raha h, chalne do!!!"

	[print("Max models in cluster: ", i, " no. of models = ", models_count[i]) for i in range(len(models_count)) if models_count[i] == max(models_count.values())]
	return [i for i in range(len(models_count)) if models_count[i] == max(models_count.values())]

cluster = return_Max_cluster()

os.system(f"/home/kartik/imp-clean/build/setup_environment.sh run_extract_models.py ../Modelling/ run_ cluster")
