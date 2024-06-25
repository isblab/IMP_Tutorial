# IMP Tutorial

This GitHub repository corresponds to the IMP workshop in [EMBO CEM3DPIP 2024](https://meetings.embo.org/event/24-cryo-em) at IISc Bangalore.

## Talks

See this [Talks folder](https://drive.google.com/drive/folders/188BHx67a8Wq53nDTanM-vWwX3X9F_OS5?usp=sharing) for all the talks.

## Related tutorials and GitHub repos

### Actin Tutorial  

[![Build Status](https://github.com/salilab/actin_tutorial/workflows/build/badge.svg?branch=main)](https://github.com/salilab/actin_tutorial/actions?query=workflow%3Abuild)

See [the IMP website](https://integrativemodeling.org/tutorials/actin/) for the complete tutorial text.

### Analysis GitHub repos

See [PMI analysis repo](https://github.com/salilab/pmi_analysis) here.

See [sampcon repo](https://github.com/salilab/sampcon) here. 

## Installation 

### IMP
https://integrativemodeling.org/doc.html

https://github.com/salilab/imp

Install binaries from here
https://integrativemodeling.org/2.21.0/doc/manual/installation.html

IMP installed via anaconda

### Chimera
Install UCSF Chimera from here 
https://www.cgl.ucsf.edu/chimera/download.html 

## Running the tutorial 

### Paths to IMP installation on the workstations at the workshop

Primarily: `/apps/conda/lib/python3.11/site-packages/IMP/`

`create_gmm.py`: `/apps/conda/lib/python3.11/site-packages/IMP/isd`

`process_output.py`: `/apps/conda/lib/python3.11/site-packages/IMP/pmi`


### Running the modeling scripts

Run from the `Play` directory. Examples:

`python3  actin_modeling_1.py out_ 1 10`

`python3 actin_modeling_2.py out_ 1 100`
