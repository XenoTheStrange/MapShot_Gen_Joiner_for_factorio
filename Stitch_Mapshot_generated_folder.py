#!/usr/bin/python3

import os
import argparse

# Parse arguments for origin and size (make them optional)
parser = argparse.ArgumentParser(description="Generate a montage of tiles within a specified region.")
parser.add_argument('-o', '--origin', help="Origin point in format #x# (e.g., -1x-1)")
parser.add_argument('-s', '--size', help="Size in format #x# (e.g., 3x3)")
parser.add_argument('dir_path', nargs='?', default="./s1zoom_4", help="Directory path containing tile images")
parser.add_argument('-d', '--dir', help="Directory path containing tile images (overrides positional argument)")
parser.add_argument('-e', '--ext', default="jpg", help="Filename extension / File format for the output image. Defaults to jpg to save space.")

args = parser.parse_args()

# Path to directory with tile images and the filler image
dir_path = args.dir if args.dir else args.dir_path
if dir_path[-1] == "/":
    dir_path = dir_path[:-1]

filler_image = "bl.png"

# Get the tile files
tile_files = [f for f in os.listdir(dir_path) if f.endswith(".jpg") and f.startswith("tile_")]

# Parse the tile files into a dictionary by coordinates
tile_map = {}
for file_name in tile_files:
    # Extract the coordinates from the file name
    parts = file_name.replace(".jpg", "").split("_")
    x, y = int(parts[1]), int(parts[2])
    tile_map[(x, y)] = file_name

# Find full bounds of the grid if no --size is given
if args.size:
    size_x, size_y = map(int, args.size.split('x'))
    min_x = min(x for x, y in tile_map.keys())
    max_x = max(x for x, y in tile_map.keys())
    min_y = min(y for x, y in tile_map.keys())
    max_y = max(y for x, y in tile_map.keys())
else:
    print(f"Assuming default tile size as one was not provided...")
    min_x = min(x for x, y in tile_map.keys())
    max_x = max(x for x, y in tile_map.keys())
    min_y = min(y for x, y in tile_map.keys())
    max_y = max(y for x, y in tile_map.keys())
    size_x = max_x - min_x + 1
    size_y = max_y - min_y + 1

# If no --origin is provided, use the center-most coordinate
if args.origin:
    origin_x, origin_y = map(int, args.origin.split('x'))
else:
    print(f"Assuming default origin as one was not provided...")
    origin_x = min_x + (max_x - min_x) // 2
    origin_y = min_y + (max_y - min_y) // 2

if (args.size and not args.origin) or (args.origin and not args.size):
    print(f"Warning: providing a size with no origin or vice-versa may result in buggy behavior")

# Calculate the bounds of the region to include based on origin and size
if args.size:
    min_x = origin_x - size_x // 2
    max_x = origin_x + size_x // 2 - (1 if size_x % 2 == 0 else 0)
    min_y = origin_y - size_y // 2
    max_y = origin_y + size_y // 2 - (1 if size_y % 2 == 0 else 0)
else:
    # If no size is specified, calculate based on the full range
    min_x = min(x for x, y in tile_map.keys())
    max_x = max(x for x, y in tile_map.keys())
    min_y = min(y for x, y in tile_map.keys())
    max_y = max(y for x, y in tile_map.keys())

# Print debug information
print(f"Selected region: Origin=({origin_x},{origin_y}), Size=({size_x},{size_y})")
print(f"Region bounds: min_x={min_x}, max_x={max_x}, min_y={min_y}, max_y={max_y}")

# Generate the command to run montage
x_tiles = abs(min_x - max_x) + 1
y_tiles = abs(min_y - max_y) + 1
tiles_arg = f"-tile {x_tiles}x{y_tiles}"

command = "montage"

# Loop through rows from top (max_y) to bottom (min_y)
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        # Add the tile if it exists, otherwise add the filler image
        image_file = tile_map.get((x, y), filler_image)
        image_path = os.path.join(dir_path, image_file) if image_file != filler_image else image_file
        command += f' "{image_path}"'
        # Debug output: show where each tile is being placed
        print(f"Placing tile at ({x},{y}) -> {image_path}")

# Add geometry and output file name
command += f' -geometry +0+0 {tiles_arg} {dir_path.split("/")[-1]}.{args.ext}'

# Print the montage command
print(command)
os.system(command)
