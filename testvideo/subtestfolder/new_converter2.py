import os
import subprocess
import time

# Set the list of file extensions to search for

FILE_EXTENSIONS = (".mp4", ".mkv", ".mov", ".avi", ".3gp", ".flv", ".mk4")

def scan_directory():
    """
    Scans the current directory for files with the specified file extensions.
    Returns a list of matching file paths.
    """

    log_messages = []

    matching_files = []

    # Iterate over all files in the current directory

    for file_name in os.listdir("."):

        # Check if the file matches one of the specified extensions

        if file_name.endswith(FILE_EXTENSIONS):

            matching_files.append(file_name)

    # Log a message if no matching files were found

    if not matching_files:

        log_messages.append("No matching files found in directory.")

        return None, log_messages

    # Log a message if there were files that did not match the specified extensions

    non_matching_files = [f for f in os.listdir(".") if f not in matching_files]

    if non_matching_files:

        log_messages.append(
            f'The following files were found but not matched: {", ".join(non_matching_files)}'
        )

    return matching_files, log_messages


def convert_files(file_paths):

    """

    Converts each file in the provided list to mp4 using FFmpeg.

    Converted files are saved to a new 'converted' directory in the parent folder.

    """

    log_messages = []

    # Create the 'converted' directory if it doesn't exist

    parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))

    converted_folder = os.path.join(parent_folder, "converted")

    if not os.path.exists(converted_folder):

        os.mkdir(converted_folder)

    # Iterate over each file in the list and attempt to convert it

    for file_path in file_paths:

        try:

            # Extract the filename and prefix

            file_name = os.path.basename(file_path)

            file_prefix, _ = os.path.splitext(file_name)

            # Generate the output file path

            output_file_path = os.path.join(converted_folder, file_prefix + ".mp4")

            # Run the FFmpeg command to convert the file

            command = f'ffmpeg -i "{file_path}" -q:v 0 "{output_file_path}"'

            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

            # Log a message indicating the file was converted successfully

            log_messages.append(
                f'"{file_name}" was converted to "{os.path.basename(output_file_path)}"'
            )

        except subprocess.CalledProcessError as e:

            # Log a message if there was an error during conversion

            log_messages.append(f'Error converting "{file_path}": {e.output.decode()}')

    return log_messages


def main():

    """

    Main function to run the program.

    """

    # Set up the log file

    log_file_name = f'conversion_log_{time.strftime("%Y%m%d_%H%M%S")}.txt'

    with open(log_file_name, "w") as log_file:

        # Scan the current directory for matching files

        matching_files, scan_log_messages = scan_directory()

        log_file.write("\n".join(scan_log_messages))

        log_file.write("\n\n")

        if not matching_files:

            return

        # Convert the matching files to mp4

        conversion_log_messages = convert_files(matching_files)

        log_file.write("\n".join(conversion_log_messages))

    print(f'Conversion complete. Log file saved to "{log_file_name}".')


if __name__ == "__main__":

    main()
