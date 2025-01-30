# MVA2025-SMOT4SB Baseline Code

## About Baseline Code

## Requirements

- Python 3.8.20
- FFmpeg (Required if using the visualizer in scripts/visualize_for_mot_sub.py)

## Usage

### Installation

#### Dataset preparation

Download the SMOT4SB dataset from [here]($DATASET_LINK), and place it under `datasets`. The directory structure should look like this:

```
datasets
└ SMOT4SB
　 ├ train
　 ├ pub_test
　 ├ private_test
　 └ annotations
```

After that, run the following command to format the dataset according to the baseline code and place it in `OC_SORT/datasets`:

```sh
python3 scripts/prepare_dataset.py
```

#### Package installation

```sh
pip3 install -r requirements.txt
pip3 install git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI
cd OC_SORT
python3 setup.py develop
```

### Training

First, get the COCO-pretrained YOLOX model from [this link](https://github.com/Megvii-BaseDetection/YOLOX/tree/0.1.0) and save them under `OC_SORT/pretrained`.

```sh
sh scripts/train.sh -f OC_SORT/exps/smot4sb.py -d 8 -b 48 --fp16 -c OC_SORT/pretrained/yolox_x.pth
```

Outputs will be saved under `YOLOX_outputs/smot4sb`.

### Prediction

To make predictions using the trained model, run the following command:

```sh
sh scripts/predict.sh -f OC_SORT/exps/smot4sb.py --path OC_SORT/datasets/SMOT4SB/pub_test --ckpt YOLOX_outputs/smot4sb/best_ckpt.pth.tar
```

Outputs will be saved under `YOLOX_outputs/smot4sb/predictions` as MOT Challenge format.

### Visualization

To visualize the predictions, run the following command:

```sh
python3 scripts/visualize_for_mot_ch.py -m YOLOX_outputs/smot4sb/results/0.txt -o prediction_0 -i OC_SORT/datasets/SMOT4SB/pub_test/0 --mp4 --show-bbox
```

This will generate a video named `prediction_0.mp4` in the cwd.
