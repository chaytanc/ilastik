#!/bin/bash

expected=$1
outputCSVPath=$2
diff <(sort {expected}) <(sort ${outputCSVPath})
ret=$?
if [[ $ret -eq 0 ]]; then
    echo "no differences"
    exit 0
else
    echo "differences were found"
    exit 1
fi