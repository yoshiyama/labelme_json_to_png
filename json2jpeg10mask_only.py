# python json2jpeg10mask_cut.py /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/kiso3001.json /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/kiso3001.png 255 /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/kiso3001_mask_cut.png /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/kiso3001_cut.png

#python json2jpeg10mask_cut.py /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/niekawa001.json /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/niekawa001.jpg 255 /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/niekawa001_mask_cut.png /mnt/c/Users/survey/Desktop/keikan_bridge/ROOT19/kiso3_niekawa_okuwa2/niekawa001_cut.png


import json
import argparse
from PIL import Image, ImageDraw
import os
import numpy as np
import base64
from labelme import utils

# Create mask function
def create_mask(data, img, fill_value):
    mask = Image.new('L', img.size)
    for shape in data['shapes']:
        if shape['label'] == 'hodoukyou':
            points = shape['points']
            points = [(int(x), int(y)) for x, y in points]  # cast to int
            ImageDraw.Draw(mask).polygon(points, fill=fill_value)
    return mask

# Main script
parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="JSON file path")
parser.add_argument("img_file", help="Image file path")
parser.add_argument("fill_value", type=int, help="Fill value for the mask")
parser.add_argument("mask_output_path", help="Mask output path")

args = parser.parse_args()

# Load JSON data
with open(args.json_file) as f:
    data = json.load(f)

# Load image
img = Image.open(args.img_file)

# Create mask
mask = create_mask(data, img, args.fill_value)

# Save mask
mask.save(args.mask_output_path)
