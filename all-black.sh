#!/usr/bin/env bash

if [ $# -lt 1 ]
then set -- black
fi

for cmd in "$@"
do find jstat t example-plugins -type f -name \*.py -print0 | xargs -r0 "$cmd"
done
