# python labelme_json_to_png.py <LabelmeのJSONファイルが入っているフォルダ.もとのjpgが入っていてもいい> -o=<出力先フォルダ> -label_file=<ラベルファイルのパス>
# python labelme_json_to_png.py kuroda -o=kuroda_output -label_file=kuroda_txt
# python labelme_json_to_png_L.py /mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1 -o=/mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1_mask -class_name=hodoukyou -pixel_value=255
# python labelme_json_to_png_L_fast.py /mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1 -o=/mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1_mask -class_name=hodoukyou -pixel_value=255

# mask画像を作成するためのスクリプト
# ラベルファイルとは、セグメンテーション対象を記載したテキストファイル。例えば、kimura_txtとかを参照してください。

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import subprocess
import shutil
import argparse
import tqdm
from PIL import Image
import numpy as np

TEMP_DIR = "temp"

parser = argparse.ArgumentParser()
parser.add_argument("json_dir", help="JSON files directory.")
parser.add_argument("-o", required=True, help="Output directory.")
parser.add_argument("-class_name", required=True, help="Class name to be masked.")
parser.add_argument("-pixel_value", required=True, type=int, help="Pixel value to fill the mask.")

args = parser.parse_args()

json_dir_path = Path(args.json_dir)
out_dir_path = Path(args.o)
class_name = args.class_name
pixel_value = args.pixel_value

assert json_dir_path.exists(), f"JSON directory does not exist: {json_dir_path}"
assert out_dir_path.exists(), f"Output directory does not exist: {out_dir_path}"

temp_dir_path = out_dir_path.joinpath(TEMP_DIR)
if not temp_dir_path.exists():
    temp_dir_path.mkdir()

def process_json(json_file_path):
    result = subprocess.run(["labelme_json_to_dataset", str(json_file_path), "-o", str(temp_dir_path)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode != 0 or result.stderr:
        print(f"Error in subprocess for file {json_file_path}: {result.stderr}")
        return

    label_png_path = temp_dir_path.joinpath("label.png")
    label_txt_path = temp_dir_path.joinpath("label_names.txt")

    if not label_png_path.exists() or not label_txt_path.exists():
        print(f"Failed to generate necessary files for {json_file_path}")
        return

    image = Image.open(str(label_png_path)).convert("P")
    image_array = np.array(image)

    class_id = None
    with open(str(label_txt_path), "r") as label_file:
        for label_num, label_name in enumerate(label_file):
            label_name = label_name.replace("\n", "")
            if label_name == class_name:
                class_id = label_num

    if class_id is None:
        print(f"No matching class id found for class {class_name} in file {json_file_path}")
        return

    image_array[image_array == class_id] = pixel_value
    new_image = Image.fromarray(image_array, mode="L")
    new_image.save(str(out_dir_path.joinpath(json_file_path.stem).with_suffix(".png")))

# Batch process: Convert JSON to PNG.
with ProcessPoolExecutor() as executor:
    list(tqdm.tqdm(executor.map(process_json, json_dir_path.glob("*.json")),
                   total=len(list(json_dir_path.glob("*.json")))))

# Post-processing.
if temp_dir_path.exists():
    shutil.rmtree(str(temp_dir_path))

print("Conversion is finished.")
