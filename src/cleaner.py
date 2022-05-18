import os
import fnmatch
import shutil
from datetime import datetime

from src.utilites import hash_from_file, scan_files


class CleanerModule:
    def prompt(self, *args):
        raise Exception("This is an interface")

    def clean(self, file_list: [str], default_option=None):
        raise Exception("This is an interface")


class MergeCleaner(CleanerModule):
    def __init__(self, folder, main_folder):
        self.folder = folder
        self.main_folder = main_folder

    def prompt(self, *args):
        result = None
        while result not in ["L", "R", "B"]:
            l_timestamp = datetime.fromtimestamp(os.stat(args[0]).st_mtime).strftime('%Y-%m-%d-%H:%M')
            r_timestamp = datetime.fromtimestamp(os.stat(args[1]).st_mtime).strftime('%Y-%m-%d-%H:%M')
            result = input(
                f"Files have the same name and not the same content:\n{args[0]} ({l_timestamp}) == {args[1]} ({r_timestamp})\n"
                f"Choose which version you want to save: L - Left version, R - Right version, B - Both versions\n")
        if result == "L":
            return 0, None
        elif result == "R":
            return 1, None
        elif result == "B":
            return 2, True

    def clean(self, folder, default_option=None):
        for file in scan_files(folder):
            head, tail = os.path.split(file)
            file_hash = hash_from_file(file)
            compared_file = os.path.join(head.replace(self.folder, self.main_folder), tail)
            if not os.path.exists(compared_file):
                shutil.copy2(file, compared_file)
            elif file_hash != hash_from_file(compared_file):
                if default_option is None:
                    selected_option, default_option = self.prompt(file, compared_file)
                else:
                    selected_option = default_option

                if selected_option == 0:
                    os.remove(compared_file)
                    shutil.copy2(file, compared_file)
                elif selected_option == 2:
                    shutil.copy2(file, compared_file + "_new")


class DuplicateFilesCleaner(CleanerModule):
    def prompt(self, *args):
        result = None
        while result not in ["L", "R", "B"]:
            l_timestamp = datetime.fromtimestamp(os.stat(args[0]).st_mtime).strftime('%Y-%m-%d-%H:%M')
            r_timestamp = datetime.fromtimestamp(os.stat(args[1]).st_mtime).strftime('%Y-%m-%d-%H:%M')
            result = input(f"Duplicate file found:\n{args[0]} ({l_timestamp}) == {args[1]} ({r_timestamp})\n"
                  f"Choose which version you want to save: L - Left version, R - Right version, B - Both versions\n")
        if result == "L":
            return 0, None
        elif result == "R":
            return 1, None
        elif result == "B":
            return 2, True

    def clean(self, folder, default_option=None):
        hash_table = {}
        for file in scan_files(folder):
            if os.stat(file).st_size != 0:
                file_hash = hash_from_file(file)
                if file_hash in hash_table.keys():
                    if default_option is None:
                        selected_option, default_option = self.prompt(file, hash_table[file_hash])
                    else:
                        selected_option = default_option

                    if selected_option == 0:
                        os.remove(hash_table[file_hash])
                        hash_table[file_hash] = file
                    elif selected_option == 1:
                        os.remove(file)
                else:
                    hash_table[file_hash] = file


class EmptyFilesCleaner(CleanerModule):
    def prompt(self, *args):
        result = None
        while result not in ["R", "I", "RA", "IA"]:
            result = input(f"File \"{args[0]}\" is empty. R - Remove, I - Ignore, RA - Remove All, IA - Ignore All\n")
        if result == "R":
            return True, None
        elif result == "I":
            return False, None
        elif result == "RA":
            return True, True
        elif result == "IA":
            return False, False

    def clean(self, folder, default_option=None):
        for file in scan_files(folder):
            if os.stat(file).st_size == 0:
                if default_option is None:
                    selected_option, default_option = self.prompt(file)
                else:
                    selected_option = default_option

                if selected_option:
                    os.remove(file)


class TempFilesCleaner(CleanerModule):
    def __init__(self, extensions):
        self.extensions = extensions

    def prompt(self, *args):
        result = None
        while result not in ["R", "I", "RA", "IA"]:
            result = input(f"File \"{args[0]}\" is probably a temporary file. R - Remove, I - Ignore, "
                           f"RA - Remove All, IA - Ignore All\n")
        if result == "R":
            return True, None
        elif result == "I":
            return False, None
        elif result == "RA":
            return True, True
        elif result == "IA":
            return False, False

    def clean(self, folder, default_option=None):
        for file in scan_files(folder):
            for extension in self.extensions:
                if fnmatch.fnmatch(file.split("/")[-1], extension):
                    if default_option is None:
                        temp_option, default_option = self.prompt(file)
                    else:
                        temp_option = default_option

                    if temp_option:
                        os.remove(file)


class ProblematicNamefilesCleaner(CleanerModule):
    def __init__(self, weird_characters, replacement):
        self.weird_characters = weird_characters
        self.replacement = replacement

    def prompt(self, *args):
        result = None
        while result not in ["Y", "N", "YA", "NO"]:
            result = input(f"Problematic character in filename: {args[0]}. Do you want to replace it? Y - Yes, "
                           f"N - No, YA - Yes for All, NO - No for All\n")
        if result == "Y":
            return True, None
        elif result == "N":
            return False, None
        elif result == "YA":
            return True, True
        elif result == "NO":
            return False, False

    def clean(self, folder, default_option=None):
        for file in scan_files(folder):
            head, tail = os.path.split(file)
            for character in self.weird_characters:
                if character in tail:
                    if default_option is None:
                        temp_option, default_option = self.prompt(file)
                    else:
                        temp_option = default_option

                    if temp_option:
                        os.rename(file, os.path.join(head, tail.replace(character, self.replacement)))


class WrongPermissionsCleaner(CleanerModule):
    def __init__(self, preferred_permissions):
        self.preferred_permissions = preferred_permissions

    def prompt(self, *args):
        result = None
        while result not in ["Y", "N", "YA", "NO"]:
            result = input(f"Wrong permissions of filename: {args[0]} ({args[1]}). "
                           f"Do you want to change to {self.preferred_permissions}? "
                           f"Y - Yes, N - No, YA - Yes for All, NO - No for All\n")
        if result == "Y":
            return True, None
        elif result == "N":
            return False, None
        elif result == "YA":
            return True, True
        elif result == "NO":
            return False, False

    def clean(self, folder, default_option=None):
        for file in scan_files(folder):
            permissions = int(oct(os.stat(file).st_mode)[-3:])
            if permissions != self.preferred_permissions:
                if default_option is None:
                    temp_option, default_option = self.prompt(file, str(permissions))
                else:
                    temp_option = default_option

                if temp_option:
                    os.chmod(file, int(str(self.preferred_permissions), 8))
