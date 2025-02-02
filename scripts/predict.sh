#!/bin/bash

cd "$(dirname "$0")/.." | exit
python3 OC_SORT/tools/predict.py "$@" --save_result --min-box-area 0 --track_thres 0.1 --iou_thresh 0.1 --use_byte True --match_thresh 0.3 --asso diou --track_buffer 50 --min_hits 1 --deltat 7 --aspect_ratio_thresh 4
