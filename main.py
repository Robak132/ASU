import json
import sys
import os
import shutil
from datetime import datetime

from src.cleaner import EmptyFilesCleaner, TempFilesCleaner, DuplicateFilesCleaner, ProblematicNamefilesCleaner, \
    WrongPermissionsCleaner, MergeCleaner
from src.utilites import scan_files, hash_from_file

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
    preferred_permissions = settings["PreferredPermissions"]

    for folder in compare_folders:
        MergeCleaner(folder, main_folder_name).clean(folder)
    print("Merging files: DONE")

    DuplicateFilesCleaner().clean(main_folder_name)
    print("Duplicate files: DONE")

    EmptyFilesCleaner().clean(main_folder_name)
    print("Empty files: DONE")

    TempFilesCleaner(temp_regex).clean(main_folder_name)
    print("Temp files: DONE")

    ProblematicNamefilesCleaner(problematic_characters, replacement).clean(main_folder_name)
    print("Problematic names: DONE")

    WrongPermissionsCleaner(preferred_permissions).clean(main_folder_name)
    print("Wrong permissions: DONE")
