import hashlib
import os
import fnmatch
from datetime import datetime

from cleaner import scan_files, rm_empty_files, rm_temp_files


def hash_file(filename):
    BUF_SIZE = 65536
    sha = hashlib.sha512()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


if __name__ == '__main__':
    main_folder_name = "../test/X"
    compare_folders = ["../test/Y1", "../test/Y2"]

    temp_regex = "*.tmp"

    file_list = scan_files(main_folder_name)
    print("Mapping files: DONE")

    save_option=None
    hash_table = {}
    for file in scan_files(main_folder_name):
        if os.stat(file).st_size != 0:
            fhash = hash_file(file)
            if fhash in hash_table.keys():
                l_timestamp = datetime.fromtimestamp(os.stat(file).st_mtime).strftime('%Y-%m-%d-%H:%M')
                r_timestamp = datetime.fromtimestamp(os.stat(hash_table[fhash]).st_mtime).strftime('%Y-%m-%d-%H:%M')
                print(f"Duplicate file found: {file} ({l_timestamp}) == {hash_table[fhash]} ({r_timestamp}). L - Left version, R - Right version")
            else:
                hash_table[fhash] = file

    for folder in compare_folders:
        for file in scan_files(folder):
            fhash = hash_file(file)
            if fhash not in hash_table.keys():
                print(f"New file found: {file}. C - Copy to base folder, M - Move to base folder, I - Ignore")

    # file_list = rm_empty_files(file_list)
    # print("Empty files: DONE")

    # file_list = rm_temp_files(file_list, temp_regex)
    # print("Temp files: DONE")

