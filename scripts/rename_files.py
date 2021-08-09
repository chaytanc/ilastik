#!/usr/bin/env python3
import sys
import os

'''
USAGE: python3 rename_files.py {path to dir containing files with spaces}
This script will rename all files in the given directory that contain
spaces to the same name but with underscores instead. Handy to have around.
'''


# Removes spaces and puts in underscores for files
def rename_files(csv_dir):
    for filename in os.listdir(csv_dir):
        new_name = filename.replace(' ', '_')
        old_file_path = os.path.join(csv_dir, filename)
        new_file_path = os.path.join(csv_dir, new_name)
        os.rename(old_file_path, new_file_path) 
        print("New name: ", new_name)


if __name__ == "__main__":
    print("args: ", str(sys.argv))
    csv_dir = sys.argv[1]
    rename_files(csv_dir)
    print("Success! damn those pesky spaces")
