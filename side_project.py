# python3
"""As the name implies, a side project to generate some video"""

import time
from pyffmpeg import FFmpeg

ff = FFmpeg()


def FFmaker():
    """Currently does precisely nothing."""

    begin = time.perf_counter()
    try:
        ff.options("-f lavfi -i color=red -frames:v 200 red_vid.mp4")
    except BaseException:
        print("Error in options function")
    end = time.perf_counter()
    print(f"File created in {end - begin:0.2f} seconds.")
