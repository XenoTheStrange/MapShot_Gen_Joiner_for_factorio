#!/usr/bin/python3

import os

# Path to directory with tile images and the filler image
dir_path = "./s1zoom_4"
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

# Find bounds of the grid
min_x = min(x for x, y in tile_map.keys())
max_x = max(x for x, y in tile_map.keys())
min_y = min(y for x, y in tile_map.keys())
max_y = max(y for x, y in tile_map.keys())

x_tiles = abs(min_x - max_x)+1
y_tiles = abs(min_y - max_y)+1
tiles_arg = f"-tile {x_tiles}x{y_tiles}"

# Print debug information
print(f"Grid bounds: min_x={min_x}, max_x={max_x}, min_y={min_y}, max_y={max_y}")

# Generate the command to run montage
command = "montage"

# Loop through rows from top (max_y) to bottom (min_y)
for y in range(min_y, max_y + 1):  # Correct order: bottom to top
    for x in range(min_x, max_x + 1):
        # Add the tile if it exists, otherwise add the filler image
        image_file = tile_map.get((x, y), filler_image)
        image_path = os.path.join(dir_path, image_file) if image_file != filler_image else image_file
        command += f' "{image_path}"'
        # Debug output: show where each tile is being placed
        print(f"Placing tile at ({x},{y}) -> {image_path}")

# Add geometry and output file name
command += f' -geometry +0+0 {tiles_arg} {dir_path.split("/")[-1]}.png'

# Print the montage command
print(command)
os.system(command)
