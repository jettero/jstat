#!/usr/bin/env bash

CMD="${1:-black}"

find jstat t example-plugins -type f -name \*.py -print0 \
    | xargs -r0 "$CMD"
