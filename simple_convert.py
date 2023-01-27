""" Initial basic conversion script"""

from pyffmpeg import FFmpeg

FILE_IN = "sample_mkv.mkv"
FILE_OUT = "converted_mkv.mp4"

ff = FFmpeg()

output_file = ff.convert(FILE_IN, FILE_OUT)

print(f'File {FILE_IN} converted to {FILE_OUT}')
