# IMP Tutorial

This github repository corresponds to the IMP workshop in [EMBO CEM3DPIP 2024](https://meetings.embo.org/event/24-cryo-em) at IISc Bangalore.

## Talks

See this [Talks folder](https://drive.google.com/drive/folders/188BHx67a8Wq53nDTanM-vWwX3X9F_OS5?usp=sharing) for all the talks.

## Related tutorials and github repos

### Actin Tutorial  

[![Build Status](https://github.com/salilab/actin_tutorial/workflows/build/badge.svg?branch=main)](https://github.com/salilab/actin_tutorial/actions?query=workflow%3Abuild)

See [the IMP website](https://integrativemodeling.org/tutorials/actin/) for the complete tutorial text.

### Analysis GitHub repo

See [PMI analysis repo](https://github.com/salilab/pmi_analysis) here.

See [sampcon repo](https://github.com/salilab/sampcon) here. 

## Installation 

### IMP
https://integrativemodeling.org/doc.html

https://github.com/salilab/imp

Install binaries from here
https://integrativemodeling.org/2.20.0/doc/manual/installation.html

### Chimera
Install UCSF Chimera from here 
https://www.cgl.ucsf.edu/chimera/download.html 

## Running the tutorial 
### Paths to IMP installation on the workstations at the workshop
#TODO

Primarily: `/usr/lib/pythonxx/dist-packages/IMP`

Some packages are at : `/usr/share`

`create_gmm.py`: `/usr/lib/pythonxx/dist-packages/IMP/isd`

`process_output.py`: `/usr/lib/pythonxx/dist-packages/IMP/pmi`

If you want to find an IMP script call `locate`.

### Running the modeling scripts
#TODO

Run from the `Play` directory. Examples:

`python3  actin_modeling_1.py out_ 1 10`

`python3 actin_modeling_2.py out_ 1 100`
