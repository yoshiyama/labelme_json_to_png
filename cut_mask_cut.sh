#!/bin/bash

INPUT_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2"
MASK_OUTPUT_DIR="/mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2_mask_cut"
PIXEL_VALUE="255"

for json_file in "$INPUT_DIR"/*.json
do
  base_name=$(basename "$json_file" .json)
  if [ -f "$INPUT_DIR/$base_name.jpg" ]; then
      img_file="$INPUT_DIR/$base_name.jpg"
  elif [ -f "$INPUT_DIR/$base_name.png" ]; then
      img_file="$INPUT_DIR/$base_name.png"
  else
      echo "Neither .jpg nor .png file found for $base_name"
      continue
  fi
  mask_output_path="$MASK_OUTPUT_DIR/$base_name_mask.png"
  cropped_img_output_path="$INPUT_DIR/$base_name"_cropped_img.png
  cropped_mask_output_path="$MASK_OUTPUT_DIR/$base_name"_cropped_mask.png

  python json2jpeg10mask_cut.py "$json_file" "$img_file" "$PIXEL_VALUE" "$mask_output_path" "$cropped_img_output_path" "$cropped_mask_output_path"
done
