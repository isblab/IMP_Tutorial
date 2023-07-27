'''
Script for integrative modeling of the actin/tropomodulin binding interface
using a topology file
'''
# Imports
from __future__ import print_function
import IMP
import IMP.pmi
import IMP.pmi.io
import IMP.pmi.io.crosslink
import IMP.pmi.topology
import IMP.pmi.macros
import IMP.pmi.restraints
import IMP.pmi.restraints.stereochemistry
import IMP.pmi.restraints.saxs
import IMP.pmi.restraints.crosslinking
import IMP.pmi.restraints.em
import IMP.pmi.dof
import IMP.atom
import IMP.saxs
import sys
import RMF


output_path = sys.argv[1]      # output file name
output_index = sys.argv[2]
num_frames = int(sys.argv[3])  # Number of frames in MC run

# Identify data files
xl_data = "../data/derived_data/xl/derived_xls.dat"
gmm_data = "../data/derived_data/em/4pki_20a_50.gmm"

# Restraint weights
xl_weight = 10.0
em_weight = 1000.0

# Topology File
topology_file = "../data/topology_test.txt"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Here is where the work begins
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# All IMP systems start out with a Model
mdl = IMP.Model()

# Read the topology file for a given state
t = IMP.pmi.topology.TopologyReader( topology_file )

# Create a BuildSystem macro to and add a state from a topology file
bs = IMP.pmi.macros.BuildSystem(mdl)
bs.add_state(t)

# executing the macro will return the root hierarchy and degrees of freedom (dof) objects
# root_hier, dof = bs.execute_macro()
root_hier, dof = bs.execute_macro(max_rb_trans=0.1,
                                  max_rb_rot=0.1,
                                  max_bead_trans=2.5,
                                  max_srb_trans=4.0,
                                  max_srb_rot=0.3)

# It's useful to have a list of the molecules.
molecules = t.get_components()

##### Uncomment the following lines to get test.rmf file to visualise the system representation
#
# # Uncomment this line for verbose output of the representation
IMP.atom.show_with_representations(root_hier)
# output to RMF
fname = 'test.rmf'
rh = RMF.create_rmf_file(fname)
IMP.rmf.add_hierarchy(rh, root_hier)
IMP.rmf.save_frame(rh)
