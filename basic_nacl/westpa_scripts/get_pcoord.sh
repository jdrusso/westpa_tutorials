#!/bin/bash
set -x
cd $WEST_SIM_ROOT/bstates || exit 1

REF_NO_XML=${WEST_STRUCT_DATA_REF%.xml}
REF_NO_EXT=${REF_NO_XML%.pdb}

env | grep WEST
env | grep REF

echo "Writing pcoord to " $WEST_PCOORD_RETURN
python $WEST_SIM_ROOT/westpa_scripts/get_pcoord.py $WEST_STRUCT_DATA_REF ${REF_NO_EXT}.pdb > $WEST_PCOORD_RETURN
# cat pcoord.init > $WEST_PCOORD_RETURN
