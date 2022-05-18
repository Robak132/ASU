import ast
import configparser
import json
import sys

from cleaner import EmptyFilesCleaner, TempFilesCleaner, DuplicateFilesCleaner, ProblematicNamefilesCleaner
from utilites import scan_files

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Not enough parameters")

    main_folder_name = sys.argv[1]
    compare_folders = sys.argv[2:]
    with open('settings.json', encoding='utf-8') as fh:
        settings = json.load(fh)
    temp_regex = settings["TempExtensions"]
    problematic_characters = settings["ProblematicCharacters"]
    replacement = settings["ProblematicCharactersReplacement"]

    file_list = scan_files(main_folder_name)
    hash_table = DuplicateFilesCleaner().clean(file_list)
    print("Duplicate files: DONE")

    for folder in compare_folders:
        for file in scan_files(folder):
            fhash = hash_file(file)
            if fhash not in hash_table.keys():
                shutil.copy2(file, file.replace(folder, main_folder_name))
            elif os.stat(file).st_size != 0:
                l_timestamp = datetime.fromtimestamp(os.stat(file).st_mtime).strftime('%Y-%m-%d-%H:%M')
                r_timestamp = datetime.fromtimestamp(os.stat(hash_table[fhash]).st_mtime).strftime('%Y-%m-%d-%H:%M')
                print(f"Conflict in merging files: {hash_table[fhash]} ({r_timestamp}) <- {file} ({l_timestamp})\n"
                      f"Choose which version you want to save: L - Left version, R - Right version, B - Both versions")

    file_list = scan_files(main_folder_name)
    EmptyFilesCleaner().clean(file_list)
    print("Empty files: DONE")

    file_list = scan_files(main_folder_name)
    TempFilesCleaner(temp_regex).clean(file_list)
    print("Temp files: DONE")

    file_list = scan_files(main_folder_name)
    ProblematicNamefilesCleaner(problematic_characters, replacement).clean(file_list)
    print("Temp files: DONE")
