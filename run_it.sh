#!/usr/bin/env bash

# This runs all of the code with a command line argument giving the number of threads to use

if [[ $# -eq 0 ]] ; then
	NUM_PY_THREADS=1
elif [[ $# -eq 1 ]] ; then
	NUM_PY_THREADS=$1
else
	echo 'Wrong number of parameters passed to xml_rewrite: only NUM_PY_THREADS needed.'
    exit 1
fi

python -m src $NUM_PY_THREADS
rm -rf unzipped_files/*