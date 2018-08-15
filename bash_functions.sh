#!/usr/bin/env bash

function unzip_dat_file {
    # will get our USPTO XML files ready for processing
    OUTDIR='./unzipped_files'
    unzip -qq -o -j "$1" -d "$OUTDIR/"
}

"$@"