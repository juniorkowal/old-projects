
import os

rootdir = '../buildings'

for subdir, dirs, files in os.walk(rootdir):
    files_in_directory = os.listdir(subdir)
    filtered_files = [file for file in files_in_directory if file.endswith(".png")]
    for file in filtered_files:
        path_to_file = os.path.join(subdir, file)
        print(path_to_file)
        os.remove(path_to_file)