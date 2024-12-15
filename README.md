# MapShot_Gen_Joiner_for_factorio
 Joins together sections of mapshot gens using imagemagick (montage) and python. Made for linux.

Argparse really doesn't like dashes in arguments so it needs the space otherwise it'll fail probably.
space and quotes not needed if not using negative numbers

Ex. ./script /path/s1zoom_4 --origin "-3 x -3" --size 4x8
    ./script /path/s1zoom_4 -o 2x4 -s 4x4
