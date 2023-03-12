import os
import json
import time
from pyffmpeg import FFmpeg

def convert_files(directory_path, ticket_number, new_extension):
    supported_extensions = [".mp4", ".mkv", ".flv", ".3gp", ".mov"]
    new_directory_path = os.path.join(directory_path, ticket_number)
    os.makedirs(new_directory_path, exist_ok=True)
    file_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            file_extension = os.path.splitext(filename)[1]
            if file_extension in supported_extensions:
                new_filename = filename[:-len(file_extension)] + new_extension
                file_list.append((filename, new_filename))
                print("The original file name is:", filename)
                print("The new file name would be:", new_filename)
            else:
                print(f"{filename} is not a supported file type for conversion")
    log_file = open(os.path.join(new_directory_path, f"conversion_log_{ticket_number}.txt"), "w")
    for i, (filename, new_filename) in enumerate(file_list):
        # Construct FFmpeg command to convert video and/or audio
        input_file = os.path.join(directory_path, filename)
        output_file = os.path.join(new_directory_path, new_filename)
        ffmpeg = FFmpeg(inputs={input_file: None}, outputs={output_file: None})
        # Call FFmpeg command
        start_time = time.time()
        print(f"Converting file {i+1} of {len(file_list)}: {filename}")
        ffmpeg.run()
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        log_file.write(f"{filename} converted to {new_filename} in {elapsed_time:.2f} seconds\n")
    log_file.close()
    with open(os.path.join(new_directory_path, "file_list.json"), "w") as f:
        json.dump(file_list, f)
