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

### Submission

To submit the predictions, you need to compress the prediction txt files into a zip file. Run the following command to do so:

```sh
python3 scripts/create_submission.py -i YOLOX_outputs/smot4sb/predictions/pub_test/
```

The submission file will be saved as `<YYYY-MM-DD_hh-mm-ss>.zip`.

### Visualization

To visualize the predictions, run the following command:

```sh
python3 scripts/visualize_for_mot_ch.py -m YOLOX_outputs/smot4sb/results/0.txt -o prediction_0 -i OC_SORT/datasets/SMOT4SB/pub_test/0 --mp4 --show-bbox
```

This will generate a video named `prediction_0.mp4` in the cwd.

### Evaluation for validation dataset

For evaluation, the ground truth (gt) and predictions must be in the format and directory structure compatible with TrackEval. The following commands prepare the necessary files:

```sh
# Make predictions on the validation data
sh scripts/predict.sh -f OC_SORT/exps/smot4sb.py --path OC_SORT/datasets/SMOT4SB/val--ckpt YOLOX_outputs/smot4sb/best_ckpt.pth.tar

# Modify the directory structure of the predictions
python scripts/cp_preds_for_eval.py -i YOLOX_outputs/smot4sb/predictions/val/ -o eval_inputs

# Prepare the gt
python3 scripts/oc_sort_ann_to_mot_ch.py -i OC_SORT/datasets/SMOT4SB/annotations/val.json -o eval_inputs
```

The conversion results will be output to the `eval_inputs` directory.

Next, evaluate using the following command:

```sh
python3 TrackEval/scripts/run_smot4sb_challenge.py eval_inputs eval_outputs val --metric-smot4sb
```

The evaluation results will be saved in the `eval_outputs` directory.
