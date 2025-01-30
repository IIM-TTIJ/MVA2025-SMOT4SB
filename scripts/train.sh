#!/bin/bash

cd "$(dirname "$0")/.." | exit
python3 OC_SORT/tools/train.py "$@"
