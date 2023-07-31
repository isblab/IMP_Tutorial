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
import ihm.cross_linkers
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
topology_file = "../data/topology.txt"

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


#####################################################
##################### RESTRAINTS ####################
#####################################################

# Restraints define functions that score the model based on
# input information.
#
# Restraint objects are first created in the definition.
# To be evaluated, the restraint object must be add_to_model().
#
# In some cases, sampled parameters for restraints must be added to the DOF
# object

# The output_objects list is used to collect all restraints
# where we want to log the output in the STAT file.
# Each restraint should be appended to this list.
output_objects = []

# -----------------------------
# %%%%% CONNECTIVITY RESTRAINT
#
# Restrains residues/particles that are collected in sequence
# This should be used for any system without an atomic force field (e.g. CHARMM)
# We apply the restraint to each molecule

for m in root_hier.get_children()[0].get_children():
    cr = IMP.pmi.restraints.stereochemistry.ConnectivityRestraint(m)
    cr.add_to_model()
    output_objects.append(cr)

# -----------------------------
# %%%%% EXCLUDED VOLUME RESTRAINT
#
# Keeps particles from occupying the same area in space.
# Here, we pass a list of both molecule chains to included_objects to apply this to every residue.
# We could also have passed root_hier to obtain the same behavior.
#
# resolution=1000 applies this expensive restraint to the lowest resolution for each particle.
evr = IMP.pmi.restraints.stereochemistry.ExcludedVolumeSphere(
                                            included_objects=[root_hier],
                                            resolution=1000 )
output_objects.append(evr)


# -------------------------
# %%%%% CROSSLINKING RESTRAINT
#
# Restrains two particles via a distance restraint based on
# an observed crosslink.
#
# First, create the crosslinking database from the input file
# The "standard keys" correspond to a crosslink csv file of the form:
#
# Protein1,Residue1,Protein2,Residue2
# A,18,G,24
# A,18,G,146
# A,50,G,146
# A,50,G,171
# A,50,G,189
#
# This restraint allows for ambiguity in the crosslinked residues,
# a confidence metric for each crosslink and multiple states.
# See the PMI documentation or the MMB book chapter for a
# full discussion of implementing crosslinking restraints.

# This first step is used to translate the crosslinking data file.
# The KeywordsConverter maps a column label from the xl data file
# to the value that PMI understands.
xldbkc = IMP.pmi.io.crosslink.CrossLinkDataBaseKeywordsConverter()
# Here, we just use the standard keys.
xldbkc.set_standard_keys()
# One can define custom keywords using the syntax below.
# For example if the Protein1 column header is "prot_1"
# xldbkc["Protein1"]="prot_1"

# The CrossLinkDataBase translates and stores the crosslink information
# from the file "xl_data" using the KeywordsConverter.
xldb = IMP.pmi.io.crosslink.CrossLinkDataBase()
xldb.create_set_from_file(file_name=xl_data,
                            converter=xldbkc)

xlr = IMP.pmi.restraints.crosslinking.CrossLinkingMassSpectrometryRestraint(
                root_hier=root_hier,    # Must pass the root hierarchy to the system
                database=xldb, # The crosslink database.
                length=25,              # The crosslinker plus side chain length
                resolution=1,           # The resolution at which to evaluate the crosslink
                slope=0.0001,           # This adds a linear term to the scoring function
                                        #   to bias crosslinks towards each other
                weight=xl_weight,       # Scaling factor for the restraint score.
                linker=ihm.cross_linkers.dss) # The linker chemistry

output_objects.append(xlr)

# -------------------------
# %%%%% EM RESTRAINT
#
# Scores a model based on its cross-correlation to an EM density.
# Since cross-sorrelation is very expensive, we approximate both
# the EM map and model as a set of 3D Gaussians (done in Representation).
#
# First, collect all density particles from the model.
densities = IMP.atom.Selection(root_hier,representation_type=IMP.atom.DENSITIES).get_selected_particles()

emr = IMP.pmi.restraints.em.GaussianEMRestraint(
             densities,                 # Evaluate the restraint using these model densities
             target_fn=gmm_data,        # The EM map, approximated as a gaussian mixture model (GMM)
             slope=0.00000001,          # a small linear restraint to pull objects towards the EM map center
             scale_target_to_mass=True, # Normalizes the total density of the model wrs: EM map. Only set to true
                                        #   if the EM map and "densities" contain the same objects.
             weight=em_weight)          # the scaling factor for the EM score

output_objects.append(emr)

#####################################################
###################### SAMPLING #####################
#####################################################
# With our representation and scoring functions determined, we can now sample
# the configurations of our model with respect to the information.

# First shuffle all particles to randomize the starting point of the
# system. For larger systems, you may want to increase max_translation
IMP.pmi.tools.shuffle_configuration(root_hier,
                                    max_translation=10)

# Shuffling randomizes the bead positions. It's good to
# allow these to optimize first to relax large connectivity
# restraint scores.  100-500 steps is generally sufficient.
dof.optimize_flexible_beads(500)

# Now, add all of the other restraints to the scoring function to start sampling
evr.add_to_model()
emr.add_to_model()
xlr.add_to_model()

# ##### Uncomment the following lines to get test.rmf file to visualise the system representation
# #
# # # Uncomment this line for verbose output of the representation
# IMP.atom.show_with_representations(root_hier)
# # output to RMF
# fname = 'Shuffle_1000.rmf'
# rh = RMF.create_rmf_file(fname)
# IMP.rmf.add_hierarchy(rh, root_hier)
# IMP.rmf.save_frame(rh)


# Run replica exchange Monte Carlo sampling
rex=IMP.pmi.macros.ReplicaExchange(mdl,
        root_hier=root_hier,                                        # pass the root hierarchy
        monte_carlo_sample_objects=dof.get_movers(),                # pass all objects to be moved ( almost always dof.get_movers() )
        global_output_directory=output_path + str(output_index),    # The output directory for this sampling run.
        output_objects=output_objects,                              # Items in output_objects write information to the stat file.
        replica_exchange_minimum_temperature=1.0,
        replica_exchange_maximum_temperature=1.25,
        monte_carlo_steps=10,                                       # Number of MC steps between writing frames
        number_of_best_scoring_models=0,                            # set >0 to store best PDB files (but this is slow)
        number_of_frames=num_frames)                                # Total number of frames to run / write to the RMF file.

# Ok, now we finally do the sampling!
rex.execute_macro()

# Outputs are then analyzed in a separate analysis script.
