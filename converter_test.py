# python3
"""Converts various input video file types to .mp4 format."""

import time
from pyffmpeg import FFmpeg

ff = FFmpeg()


class FFMConverter:
    """FFmpeg class"""

    def to_mp4_pyffmpeg(self, input_file, output_file):
        """Using pyffmpeg's native '.convert' method. Reduces file size"""
        begin = time.perf_counter()
        try:
            ff.convert(input_file, output_file)
        except BaseException:
            print("Error in pyffmpeg function")
        end = time.perf_counter()
        print(
            f"File {input_file} converted to {output_file} in {end - begin:0.2f} seconds."
        )

    def to_mp4_options(self, input_file, output_file):
        """Using .options pyffmpeg method.  This changes encoding of both
        video and audio streams.  Experimental only to compare ff.options
        method versus straight ff.convert method. Manipulation probably
        won't be done in production. However, using the .options method
        provides the ability to specify more granular detail."""
        begin = time.perf_counter()
        try:
            ff.options(f"-i {input_file} -c:v libx264 -c:a aac {output_file}")
        except BaseException:
            print("Error in options function")
        end = time.perf_counter()
        print(
            f"File {input_file} converted to {output_file} in {end - begin:0.2f} seconds."
        )

    def to_mp4_options_copy(self, input_file, output_file):
        """Using a specific 'copy' .options method to directly transcode original
        video and audio. Seems to have no effect on file size or quality but
        processes quite a bit faster than either of the other methods.  Does not
        work for .ogx at this time."""
        begin = time.perf_counter()
        try:
            ff.options(f"-i {input_file} -c:v copy -c:a copy {output_file}")
        except BaseException:
            print("Error in options_copy function")
        end = time.perf_counter()
        print(
            f"File {input_file} converted to {output_file} in {end - begin:0.2f} seconds."
        )


ffm = FFMConverter()

ffm.to_mp4_pyffmpeg("sample-ogv-file.ogx", "pyffmpeg_converted_ogv.mp4")

ffm.to_mp4_options("sample-ogv-file.ogx", "options_converted_ogv.mp4")

ffm.to_mp4_options_copy("sample-ogv-file.ogx", "options_copyconverted_ogv.mp4")
