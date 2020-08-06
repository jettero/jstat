#!/usr/bin/env bash

find jstat t example-plugins -type f -name \*.py -print0 \
    | xargs -r0 black
