#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

#ln -sv $WEST_SIM_ROOT/common_files/bstate.pdb .

# If this segment is a continuation of a parent, then copy seg.xml which stores the parent state
# If this segment is the beginning of a new trajectory, then $WEST_PARENT_DATA_REF points to...

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
# EXPERIMENTAL if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOAFDSINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/nacl_prod.py > nacl_prod.py
  ln -sv $WEST_PARENT_DATA_REF/seg.xml ./parent.xml
  ln -sv $WEST_SIM_ROOT/common_files/bstate.pdb .
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/nacl_prod.py > nacl_prod.py
#  ln -sv $WEST_PARENT_DATA_REF ./parent.xml
#  ln -sv $WEST_SIM_ROOT/bstates/bstate.xml ./parent.xml
  ln -sv $WEST_PARENT_DATA_REF bstate.pdb

  # Now I should make $WEST_PARENT_DATA_REF into a parent.xml XML with OpenMM
  #   Is it correct to pass $WEST_RAND16, since the parent will have used a  different random seed?
  #     Well, the random seed is used to set velocities and to jitter positions
  #     If I don't set it here, and I just use the PDB instead of creating an XML,
  #     then when nacl_prod.py runs, it'll set up the system using the random seed there
  #   I should get an identical result doing it here, because it would initialize the
  #     system with the same seed later anyways.
  python $WEST_SIM_ROOT/common_files/pdb_to_xml.py bstate.pdb $WEST_RAND16

  # Now bstate.pdb and parent.xml always exist

fi

# Run the dynamics with OpenMM
python nacl_prod.py

#Calculate pcoord with MDAnalysis
python $WEST_SIM_ROOT/common_files/get_distance.py
cat dist.dat > $WEST_PCOORD_RETURN && rm -f bstate.pdb dist.dat nacl_prod.py

# Clean up
#rm -f parent.xml bstate.pdb dist.dat nacl_prod.py
#rm -f bstate.pdb dist.dat nacl_prod.py
