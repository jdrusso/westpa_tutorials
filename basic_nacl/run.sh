#!/bin/bash

# Make sure environment is set
source env.sh

# Clean up
rm -f west.log

# Run w_run
#w_run --work-manager processes "$@" # &> west.log
#w_run --work-manager processes --n-workers 4 # "$@" # &> west.log
w_run --work-manager threads --n-workers 4 # "$@" # &> west.log
