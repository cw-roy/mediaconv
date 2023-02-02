# python3

"""This script will detect container information"""

from pyffmpeg import FFprobe

input_file = "/Users/n0174972/code/mediaconv/sample_flv.flv"

fp = FFprobe(input_file)
codec = fp.metadata[0][1]['codec']

print(codec)

