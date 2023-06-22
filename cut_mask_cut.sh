#!/bin/bash

# Paths
JSON_IMG_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2"
CROPPED_MASK_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2_mask_cut"  # REPLACE with the path to your mask output directory
CROPPED_IMG_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2_png_cut"    # REPLACE with the path to your image output directory

# Pixel fill value
FILL_VALUE=255

# Python script
PYTHON_SCRIPT="json2jpeg10mask_cut.py"

for json_file in $JSON_IMG_DIR/*.json; do
  base_name=$(basename $json_file .json)

  # Check for corresponding png file
  if [ -f "$JSON_IMG_DIR/$base_name.png" ]; then
    img_file="$JSON_IMG_DIR/$base_name.png"
  elif [ -f "$JSON_IMG_DIR/$base_name.jpg" ]; then
    img_file="$JSON_IMG_DIR/$base_name.jpg"
  else
    echo "No corresponding png or jpg file for $json_file"
    continue
  fi

  cropped_mask_output_path="$CROPPED_MASK_DIR/${base_name}_mask_cut.png"
  cropped_img_output_path="$CROPPED_IMG_DIR/${base_name}_cut.png"

  python $PYTHON_SCRIPT $json_file $img_file $FILL_VALUE $cropped_mask_output_path $cropped_img_output_path
done
