#!/bin/bash

for YEAR in {1976..2001}
do
    COUNT=`ls dat_files/"$YEAR".zip 2> /dev/null | wc -l`
    while [ "$COUNT" -lt 1 ]; do
        `wget -q -r -l1 -nd -P ./dat_files/ --no-parent -A "$YEAR.zip" "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/$YEAR/"`
        COUNT=`ls dat_files/"$YEAR".zip 2> /dev/null | wc -l`
    done
done
