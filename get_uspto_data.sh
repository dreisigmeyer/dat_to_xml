#!/bin/bash

# This will download the data files from the USPTO

PATH_TO_DAT=`dirname $(readlink -f $0)`
for YEAR in {1976..2001}
do
    COUNT=`ls "$PATH_TO_DAT"/dat_files/"$YEAR".zip 2> /dev/null | wc -l`
    while [ "$COUNT" -lt 1 ]; do
        `wget -q -r -l1 -nd -P "$PATH_TO_DAT"/dat_files/ --no-parent -A "$YEAR.zip" "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/$YEAR/"`
        COUNT=`ls "$PATH_TO_DAT"/dat_files/"$YEAR".zip 2> /dev/null | wc -l`
    done
done
