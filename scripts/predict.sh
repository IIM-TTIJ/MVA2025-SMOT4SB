#!/bin/bash

cd "$(dirname "$0")/.." | exit
python3 OC_SORT/tools/predict.py "$@" --save_result --min-box-area 0
