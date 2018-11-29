#!/usr/bin/env bash

# Function use in src/dat_to_xml.py/convert_to_xml

function unzip_dat_file {
    # will get our USPTO XML files ready for processing
    OUTDIR='./unzipped_files'
    unzip -qq -o -j "$1" -d "$OUTDIR/"
}

"$@"