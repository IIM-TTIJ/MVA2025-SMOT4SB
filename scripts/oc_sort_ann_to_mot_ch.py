import argparse
import configparser
import csv
import json
import os


def main():
    parser = argparse.ArgumentParser(
        description="Convert OC SORT annotation to MOT Challenge format."
    )
    parser.add_argument("--input-file", "-i", type=str, required=True)
    parser.add_argument("--output-dir", "-o", type=str, required=True)
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        anno_json = json.load(f)

    csv_dict, seq_length_dict = convert(anno_json)
    for k, v in csv_dict.items():
        gt_dir = f"{args.output_dir}/{k}/gt"
        os.makedirs(gt_dir, exist_ok=True)
        with open(f"{gt_dir}/gt.txt", "w") as f:
            writer = csv.writer(f)
            writer.writerows(v)
        config = configparser.ConfigParser()
        config["Sequence"] = {
            "name": k,
            "imDir": "img1",
            "frameRate": 30,
            "seqLength": seq_length_dict[k],
            "imWidth": 3840,
            "imHeight": 2160,
            "imExt": ".jpg",
        }
        with open(f"{args.output_dir}/{k}/seqinfo.ini", "w") as f:
            config.write(f)


def convert(anno_json):
    videos = anno_json["videos"]
    video_id_to_name = {x["id"]: os.path.basename(x["name"]) for x in videos}
    video_indices = [x["id"] for x in videos]

    result = {k: [] for k in video_indices}
    seq_length_dict = {k: 0 for k in video_indices}

    image_video_map = {}
    for image in anno_json["images"]:
        video_id = image["video_id"]
        image_id = image["id"]
        image_video_map[image_id] = video_id

    images_dict = {}
    for image in anno_json["images"]:
        video_id = image["video_id"]
        if video_id not in images_dict:
            images_dict[video_id] = []
        images_dict[video_id].append(image)
        seq_length_dict[video_id] += 1
    for images in images_dict.values():
        images.sort(key=lambda x: x["id"])
        for i, x in enumerate(images, 1):
            x["id"] = i

    for annotation in anno_json["annotations"]:
        image_id = annotation["image_id"]
        video_id = image_video_map[image_id]
        if video_id not in result:
            result[video_id] = []
        result[video_id].append(annotation)

    for k, v in result.items():
        v.sort(key=lambda x: x["id"])
        for i, x in enumerate(v, 1):
            x["id"] = i

    csv_dict = {k: [] for k in video_indices}
    for k, v in result.items():
        for annotation in v:
            csv_dict[k].append(
                [
                    annotation["image_id"],
                    annotation["track_id"],
                    annotation["bbox"][0],
                    annotation["bbox"][1],
                    annotation["bbox"][2],
                    annotation["bbox"][3],
                    -1,
                    -1,
                    -1,
                    -1,
                ]
            )

    return {video_id_to_name[k]: v for k, v in csv_dict.items()}, {
        video_id_to_name[k]: v for k, v in seq_length_dict.items()
    }


if __name__ == "__main__":
    main()
