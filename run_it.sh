#!/usr/bin/env bash

NUM_PY_THREADS=4
python -m src $NUM_PY_THREADS
rm -rf unzipped_files/*