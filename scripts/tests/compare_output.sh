#!/bin/bash

expected=$1
outputCSVPath=$2
#diff <(sort ${expected}) <(sort ${outputCSVPath})
# Diff which ignores comments and blank line differences using process substitution
diff -u -B <(grep -vE '^\s*(#|$)' ${expected} | sort)  <(grep -vE '^\s*(#|$)' ${outputCSVPath} | sort)
ret=$?
if [[ $ret -eq 0 ]]; then
    echo "no differences"
    exit 0
else
    echo "differences were found"
    exit 1
fi