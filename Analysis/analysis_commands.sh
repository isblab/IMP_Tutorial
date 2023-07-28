#!/bin/bash

# PMI analysis
python run_analysis_trajectories.py ../Modeling/ output_

# Variable Filter
python variable_filter_v1.py -c 0

# Model Extraction
python run_extract_models.py ../Modeling/ output_ 0

# Sampcon
python sampcon_path -n actin -m cpu_omp -c 4 -d density_file -gp -g 5 -sa model_analysis/A_models_clust0.txt -sb model_analysis/B_models_clust0.txt -ra model_analysis/A_models_clust0.rmf3 -rb model_analysis/B_models_clust0.rmf3 --align