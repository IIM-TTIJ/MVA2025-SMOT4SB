import argparse
import configparser
import csv
import json
import os


def main():
    parser = argparse.ArgumentParser(
        description="Convert OC-SORT annotation to MOT Challenge format."
    )
    parser.add_argument("--input-file", "-i", type=str, required=True)
    parser.add_argument("--output-dir", "-o", type=str, default="eval_inputs")
    parser.add_argument("--subset", "-s", type=str)
    args = parser.parse_args()

    ref_dir = os.path.join(args.output_dir, "ref")

    with open(args.input_file, "r") as f:
        anno_json = json.load(f)

    if args.subset is None:
        subset = os.path.splitext(os.path.basename(args.input_file))[0]
    else:
        subset = args.subset
    subset_dir = f"{ref_dir}/{subset}"

    image_video_map = {image["id"]: image["video_id"] for image in anno_json["images"]}
    videos = anno_json["videos"]

    seq_maps = ["name"]
    for video in videos:
        gt, seq_length = convet(anno_json, image_video_map, video["id"])

        video_name = video["name"]
        video_dir = f"{subset_dir}/{video_name}"
        gt_dir = f"{video_dir}/gt"
        os.makedirs(gt_dir, exist_ok=True)

        write_gt(gt, gt_dir)
        write_seqinfo(video_name, seq_length, video_dir)
        seq_maps.append(video_name)

        print(f"Converted {video_name}, {len(seq_maps) - 1}/{len(videos)}")

    write_seqmaps(seq_maps, subset, ref_dir)

    print(f"Done. Output is saved in {args.output_dir}")


def write_gt(gt, gt_dir):
    with open(f"{gt_dir}/gt.txt", "w") as f:
        writer = csv.writer(f)
        writer.writerows(gt)


def write_seqinfo(name, seq_length, video_dir):
    config = configparser.ConfigParser()
    config["Sequence"] = {
        "name": name,
        "imDir": "img1",
        "frameRate": 30,
        "seqLength": seq_length,
        "imWidth": 3840,
        "imHeight": 2160,
        "imExt": ".jpg",
    }
    with open(f"{video_dir}/seqinfo.ini", "w") as f:
        config.write(f)


def write_seqmaps(names, subset_name, ref_dir):
    os.makedirs(f"{ref_dir}/seqmaps", exist_ok=True)
    with open(f"{ref_dir}/seqmaps/{subset_name}.txt", "w") as f:
        f.write("\n".join(names) + "\n")


def convet(anno_json, image_video_map, target_video_id):
    target_images = [x for x in anno_json["images"] if x["video_id"] == target_video_id]
    target_images.sort(key=lambda x: x["id"])
    seq_length = len(target_images)

    min_image_id = target_images[0]["id"]
    image_id_map = {x["id"]: x["id"] - min_image_id + 1 for x in target_images}

    gt = []
    for annotation in anno_json["annotations"]:
        image_id = annotation["image_id"]
        video_id = image_video_map[image_id]
        if video_id != target_video_id:
            continue
        gt.append(
            [
                image_id_map[image_id],
                annotation["track_id"],
                annotation["bbox"][0],
                annotation["bbox"][1],
                annotation["bbox"][2],
                annotation["bbox"][3],
                1,
                1,
                1,
            ]
        )

    return gt, seq_length


if __name__ == "__main__":
    main()
