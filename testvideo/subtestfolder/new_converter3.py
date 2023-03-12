import os
import subprocess
import time

# Set the list of file extensions to search for
FILE_EXTENSIONS = (".mp4", ".mkv", ".mov", ".avi", ".3gp", ".flv", ".mk4")


def scan_directory(log_file):
    """
    Scans the current directory for files with the specified file extensions.
    Returns a list of matching file paths.
    """
    matching_files = []
    log_messages = []

    # Iterate over all files in the current directory
    for file_name in os.listdir("."):
        # Check if the file matches one of the specified extensions
        if file_name.endswith(FILE_EXTENSIONS):
            matching_files.append(file_name)

    # Log a message if no matching files were found
    if not matching_files:
        message = "No matching files found in directory."
        log_messages.append(message)
        log_file.write(message + "\n")
        raise Exception(message)

    # Log a message if there were files that did not match the specified extensions
    non_matching_files = [f for f in os.listdir(".") if f not in matching_files]
    if non_matching_files:
        message = f'Files found but not matched: {", ".join(non_matching_files)}'
        log_messages.append(message)
        log_file.write(message + "\n")

    return matching_files, log_messages

def convert_files(file_paths, log_file):
    """
    Converts each file in the provided list to mp4 using FFmpeg.
    Converted files are saved to a new 'converted' directory in the parent folder.
    """
    # Create the 'converted' directory if it doesn't exist
    parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
    converted_folder = os.path.join(parent_folder, "converted")
    if not os.path.exists(converted_folder):
        os.mkdir(converted_folder)

    log_messages = []
    start_time = time.time()

    # Iterate over each file in the list and attempt to convert it
    for file_path in file_paths:
        try:
            # Extract the filename and prefix
            file_name = os.path.basename(file_path)
            file_prefix, _ = os.path.splitext(file_name)

            # Generate the output file path
            output_file_path = os.path.join(converted_folder, file_prefix + ".mp4")

            # Run the FFmpeg command to convert the file asynchronously
            command = f'ffmpeg -i "{file_path}" -q:v 0 "{output_file_path}"'
            start_file_time = time.time()
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # Wait for the command to complete and retrieve the output
            output, _ = process.communicate()
            end_file_time = time.time()
            elapsed_file_time = end_file_time - start_file_time

            # Log a message indicating the file was converted successfully
            log_messages.append(
                f'"{file_name}" was converted to "{os.path.basename(output_file_path)}" in {elapsed_file_time:.2f} seconds'
            )
            log_file.write(
                f'"{file_name}" was converted to "{os.path.basename(output_file_path)}" in {elapsed_file_time:.2f} seconds\n'
            )
            log_file.flush()  # flush the log file buffer to write immediately
            
            # Print the elapsed time for the file to the console
            print(f'"{file_name}" converted in {elapsed_file_time:.2f} seconds')

        except subprocess.CalledProcessError as cpe:
            # Log a message if there was an error during conversion
            log_messages.append(
                f'Error converting "{file_path}": {cpe.output.decode()}'
            )
            log_file.write(f'Error converting "{file_path}": {cpe.output.decode()}\n')

    end_time = time.time()
    elapsed_time = end_time - start_time
    log_file.write(f"Elapsed time: {elapsed_time/60:.2f} minutes\n")
    print(f"Total elapsed time for batch: {elapsed_time/60:.2f} minutes")
    return log_messages


def main():
    """
    Main function to run the program
    """

    with open("conversion.log", "w", encoding="utf-8") as log_file:
        # Scan the directory for files to convert
        matching_files, log_messages = scan_directory(log_file)

        # Convert the matching files
        if matching_files:
            log_messages += convert_files(matching_files, log_file)

        # Log a message indicating the program has finished
        log_messages.append("Program finished.")
        log_file.write("Program finished.\n")

    # Print the log messages to the console
    print("\n".join(log_messages))


if __name__ == "__main__":
    main()
