#!/bin/bash
INPUT_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1"
OUTPUT_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/CycleGAN_Mask/ROOT41/kiritori-gero1_mask1"
CLASS_NAME="hodoukyou"
PIXEL_VALUE="255"

for json_file in "$INPUT_DIR"/*.json
do
  python labelme_json_to_png_L_fast.py "$json_file" -o="$OUTPUT_DIR" -class_name="$CLASS_NAME" -pixel_value="$PIXEL_VALUE"
done
