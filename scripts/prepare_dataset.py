import argparse
import json
import os
import os.path as osp

TRAIN_VAL_RATIO = (0.8, 0.2)
SRC_DIR = "datasets/SMOT4SB"
DEST_DIR = "OC_SORT/datasets/SMOT4SB"


def filter_by_video_ids(anno, target_video_names):
    video_ids = {
        video["id"] for video in anno["videos"] if video["name"] in target_video_names
    }
    images = [img for img in anno["images"] if img["video_id"] in video_ids]
    image_ids = {img["id"] for img in images}
    annotations = [ann for ann in anno["annotations"] if ann["image_id"] in image_ids]
    videos = [video for video in anno["videos"] if video["id"] in video_ids]

    return {
        "images": images,
        "annotations": annotations,
        "videos": videos,
        "categories": anno["categories"],
    }


def split_train_dir(train_video_names, val_video_names):
    os.makedirs(f"{DEST_DIR}/train", exist_ok=True)
    os.makedirs(f"{DEST_DIR}/val", exist_ok=True)

    for video_name in train_video_names:
        os.symlink(
            osp.abspath(f"{SRC_DIR}/train/{video_name}"),
            f"{DEST_DIR}/train/{video_name}",
        )

    for video_name in val_video_names:
        os.symlink(
            osp.abspath(f"{SRC_DIR}/train/{video_name}"), f"{DEST_DIR}/val/{video_name}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Prepare the dataset to match the baseline code."
    )
    _ = parser.parse_args()

    with open(f"{SRC_DIR}/annotations/train.json", "r") as f:
        train_anno = json.load(f)

    videos = train_anno["videos"]
    train_video_names = [
        video["name"] for video in videos[: int(len(videos) * TRAIN_VAL_RATIO[0])]
    ]
    val_video_names = [
        video["name"] for video in videos[int(len(videos) * TRAIN_VAL_RATIO[0]) :]
    ]

    splitted_train_anno = filter_by_video_ids(train_anno, train_video_names)
    splitted_val_anno = filter_by_video_ids(train_anno, val_video_names)

    os.makedirs(f"{DEST_DIR}", exist_ok=True)
    os.symlink(osp.abspath(f"{SRC_DIR}/pub_test"), f"{DEST_DIR}/pub_test")
    split_train_dir(train_video_names, val_video_names)

    os.makedirs(f"{DEST_DIR}/annotations", exist_ok=True)
    with open(f"{DEST_DIR}/annotations/train.json", "w") as f:
        json.dump(splitted_train_anno, f)
    with open(f"{DEST_DIR}/annotations/val.json", "w") as f:
        json.dump(splitted_val_anno, f)


if __name__ == "__main__":
    main()
