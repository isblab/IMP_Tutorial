#@title 3.2.2 Create and set up model object from topology file
import os
system_name = "actin_gelsolin_tropomodulin_complex" #@param{type: "string"}
force_create_gmm_files = True #param{type: "boolean"}
os.makedirs("/content/IMP_Tutorial/actin_tutorial-clean/modeling/gmm_files", exist_ok=True)

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
import IMP.pmi.restraints.crosslinking
import IMP.pmi.restraints.em
import IMP.pmi.dof
import ihm.cross_linkers
import IMP.atom
import sys

topology_file = "/content/IMP_Tutorial/actin_tutorial-clean/modeling/topology.txt"

# All IMP systems start out with a Model
mdl = IMP.Model()

# Read the topology file for a given state
t = IMP.pmi.topology.TopologyReader(topology_file)

# Create a BuildSystem macro to add a state from a topology file
bs = IMP.pmi.macros.BuildSystem(
    mdl,
    force_create_gmm_files=force_create_gmm_files,
    name=system_name,
)
bs.add_state(t)

# executing the macro will return the root hierarchy and degrees of freedom (dof) objects
root_hier, dof = bs.execute_macro()

# # It's useful to have a list of the molecules.
# molecules = t.get_components()

output_objects = []

################################################################################
# RESTRAINTS
################################################################################

#@title Code for crosslinking restraint
#@title Parameters

# Identify data files
xl_data = "../data/xl/derived_xls.dat" #@param {type: "string"}

# Restraint weights
xl_weight = 10.0

xldbkc = IMP.pmi.io.crosslink.CrossLinkDataBaseKeywordsConverter()
# Here, we just use the standard keys.
xldbkc.set_standard_keys()
# One can define custom keywords using the syntax below.
# For example if the Protein1 column header is "prot_1"
# xldbkc["Protein1"]="prot_1"

# The CrossLinkDataBase translates and stores the crosslink information
# from the file "xl_data" using the KeywordsConverter.
xldb = IMP.pmi.io.crosslink.CrossLinkDataBase()
xldb.create_set_from_file(
    file_name=xl_data,
    converter=xldbkc
)

xlr = IMP.pmi.restraints.crosslinking.CrossLinkingMassSpectrometryRestraint(
    root_hier=root_hier,    # Must pass the root hierarchy to the system
    database=xldb,          # The crosslink database.
    length=25,              # The crosslinker plus side chain length
    resolution=1,           # The resolution at which to evaluate the crosslink
    slope=0.0001,           # This adds a linear term to the scoring function
                            #   to bias crosslinks towards each other
    weight=xl_weight,       # Scaling factor for the restraint score.
    linker=ihm.cross_linkers.dss)  # The linker chemistry.
                              ##TODO common xlinkers

xlr.add_to_model()
output_objects.append(xlr)

#@title Code for EM restraint

# Path where the gmm data is stored
gmm_data = "../data/em/4pki_20a_34.txt" #@param {type: "string"}

# Restraint weights
em_weight = 1000.0 #param {type: "number"}
em_slope = 0.00000001 #@param {type: "number"}
scale_target_to_mass = True #param {type: "boolean"}

# First, collect all density particles from the model.
densities = IMP.atom.Selection(
    root_hier,
    representation_type=IMP.atom.DENSITIES
).get_selected_particles()

emr = IMP.pmi.restraints.em.GaussianEMRestraint(
    densities,
    target_fn=gmm_data,
    slope=em_slope,
    scale_target_to_mass=scale_target_to_mass,
    weight=em_weight
)

# emr.set_label("Act_Gel_Trop")

emr.add_to_model()
output_objects.append(emr)

#@title Code for Connectiviy restraint

for m in root_hier.get_children()[0].get_children():
    cr = IMP.pmi.restraints.stereochemistry.ConnectivityRestraint(m)
    cr.add_to_model()
    output_objects.append(cr)

#@title Code for Excluded volume restraint
evr = IMP.pmi.restraints.stereochemistry.ExcludedVolumeSphere(
    included_objects=[root_hier],
    resolution=1000
)

# Add all of the other restraints to the scoring function to start sampling
evr.add_to_model()
output_objects.append(evr)

#@title Code for shuffling and optimization
IMP.pmi.tools.shuffle_configuration(
    root_hier,
    max_translation=50
)

dof.optimize_flexible_beads(500)

################################################################################
# Sampling
################################################################################

#@title Parameters

num_frames = 150 #@param {type:"integer"}

mc_steps= 10 #@param {type:"integer"}

best_scoring_models = 1 #@param {type:"integer"}

#@title Code for replica exchange Monte Carlo sampling

test_mode = False

rex = IMP.pmi.macros.ReplicaExchange(
    mdl,
    # pass the root hierarchy
    root_hier=root_hier,
    # pass all objects to be moved ( almost always dof.get_movers() )
    monte_carlo_sample_objects=dof.get_movers(),
    # The output directory for this sampling run.
    global_output_directory='run1/output/',
    # Items in output_objects write information to the stat file.
    output_objects=output_objects,
    # Number of MC steps between writing frames
    monte_carlo_steps=mc_steps,
    # set >0 to store best PDB files (but this is slow)
    number_of_best_scoring_models= best_scoring_models,
    # Total number of frames to run / write to the RMF file.
    number_of_frames=num_frames,
    # Run in test mode (don't write anything)
    test_mode=test_mode)

# Ok, now we finally do the sampling!
rex.execute_macro()

# print(sr.evaluate())
# print(emr.evaluate())
# print(xlr.evaluate())

# Outputs are then analyzed in a separate analysis script.