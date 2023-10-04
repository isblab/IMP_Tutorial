# IMP Tutorial

This github repository corresponds to the [IMP workshop](https://sites.google.com/acads.iiserpune.ac.in/masfe/program/workshop?authuser=0) in [MASFE 2023](https://sites.google.com/acads.iiserpune.ac.in/masfe/) at IISER Pune.

## Talks

See this [Talks folder](https://drive.google.com/drive/folders/188BHx67a8Wq53nDTanM-vWwX3X9F_OS5?usp=sharing) for all the talks.

## Related tutorials and github repos
### Actin Tutorial  

[![Build Status](https://github.com/salilab/actin_tutorial/workflows/build/badge.svg?branch=main)](https://github.com/salilab/actin_tutorial/actions?query=workflow%3Abuild)

See [the IMP website](https://integrativemodeling.org/tutorials/actin/) for the complete tutorial text.

### Custom restraints GitHub repo

See [Tanmoy's repo](https://github.com/tanmoy7989/masfe2023_workshop) for the code related to his talk/demo. 

### Crosslinks restraint : RNA Pol3 repo

See [here](https://github.com/Pellarin/imp_tutorial_pol3) for the repo related to Riccardo's talk. 


### PMI analysis GitHub repo

See [Ignacias repo](https://github.com/salilab/pmi_analysis), part of IMP, for the code related to her talk.

## IMP installation and resources
https://integrativemodeling.org/doc.html

https://github.com/salilab/imp

https://integrativemodeling.org/2.19.0/doc/manual/installation.html

### Paths to IMP installation on the workstations at the workshop

Primarily: `/usr/lib/pythonxx/dist-packages/IMP`

Some packages are at : `/usr/share`

`create_gmm.py`: `/usr/lib/pythonxx/dist-packages/IMP/isd`

`process_output.py`: `/usr/lib/pythonxx/dist-packages/IMP/pmi`

If you want to find an IMP script call `locate`.

## Running the modeling scripts

Run from the `Play` directory. Examples:

`python3  actin_modeling_1.py out_ 1 10`

`python3 actin_modeling_2.py out_ 1 100`
