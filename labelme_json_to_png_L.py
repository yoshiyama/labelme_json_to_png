# python labelme_json_to_png.py <LabelmeのJSONファイルが入っているフォルダ.もとのjpgが入っていてもいい> -o=<出力先フォルダ> -label_file=<ラベルファイルのパス>
# python labelme_json_to_png.py kuroda -o=kuroda_output -label_file=kuroda_txt
# python labelme_json_to_png_L.py /mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1 -o=/mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1_mask -class_name=hodoukyou -pixel_value=255

#
# ラベルファイルとは、セグメンテーション対象を記載したテキストファイル。例えば、kimura_txtとかを参照してください。

from pathlib import Path
import subprocess
import shutil
import argparse
import tqdm
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

assert json_dir_path.exists(), "JSON directory does not exist."
assert out_dir_path.exists(), "Output directory does not exist."

temp_dir_path = out_dir_path.joinpath(TEMP_DIR)
if not temp_dir_path.exists():
    temp_dir_path.mkdir()

# Batch process: Convert JSON to PNG.
for json_file_path in tqdm.tqdm(list(json_dir_path.glob("*.json"))):
    subprocess.run(["labelme_json_to_dataset", str(json_file_path), "-o", str(temp_dir_path)], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)

    # image = Image.open(str(temp_dir_path.joinpath("label.png"))).convert("L")
    image = Image.open(str(temp_dir_path.joinpath("label.png"))).convert("P")
    # plt.imshow(image, cmap='gray')
    # plt.show()
    image_array = np.array(image)
    # plt.imshow(image_array, cmap='gray')
    # plt.show()

    class_id = None
    with open(str(temp_dir_path.joinpath("label_names.txt")), "r") as label_file:
        for label_num, label_name in enumerate(label_file):
            label_name = label_name.replace("\n", "")
            if label_name == class_name:
                class_id = label_num
                print(f"Class '{class_name}' found as class ID {class_id} in {json_file_path}")

    if class_id is not None:
        print("class_id=", class_id)
        print("pixel_value=", pixel_value)
        image_array[image_array == class_id] = pixel_value
        # plt.imshow(image_array, cmap='gray')
        # plt.show()
        new_image = Image.fromarray(image_array, mode="L")
        # plt.imshow(new_image, cmap='gray')
        # plt.show()
        new_image.save(str(out_dir_path.joinpath(json_file_path.stem).with_suffix(".png")))
        print(f"Image saved to {str(out_dir_path.joinpath(json_file_path.stem).with_suffix('.png'))}")
    else:
        print(f"Class '{class_name}' not found in {json_file_path}")

# Post-processing.
if temp_dir_path.exists():
    shutil.rmtree(str(temp_dir_path))

print("Conversion is finished.")
