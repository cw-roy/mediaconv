# python3
"""Converts various input video file types to .mp4 format."""

import time
from pyffmpeg import FFmpeg

ff = FFmpeg()

class FFMConverter:
    """FFmpeg class"""

    def to_mp4_pyffmpeg(self, input_file, output_file):
        """Using pyffmpeg's native method.  No modifications, other than
        format conversion."""
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
        """Using .options pyffmpeg method, resized. Experimental only to
        compare ff.options method versus straight ff.convert method.
        Resizing probably won't be done in production. However, using the
        .options method provides the option for more granular detail."""
        begin = time.perf_counter()
        try:
            ff.options(f"-i {input_file} -vf scale=720:-1 -c:a copy {output_file}")
        except BaseException:
            print("Error in options function")
        end = time.perf_counter()
        print(
            f"File {input_file} converted to {output_file} in {end - begin:0.2f} seconds."
        )


ffm = FFMConverter()
ffm.to_mp4_pyffmpeg("sample_3gp.3gp", "converted_3gp.mp4")
# ffm.to_mp4_options("sample_3gp.3gp", "converted_3gp.mp4")
