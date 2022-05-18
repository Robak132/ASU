import os
import fnmatch
from datetime import datetime

from utilites import hash_file


class CleanerModule:
    def prompt(self, filename: str, filename_2: str = ""):
        raise Exception("This is an interface")

    def clean(self, file_list: [str], default_option=None):
        raise Exception("This is an interface")


class DuplicateFilesCleaner(CleanerModule):
    def prompt(self, filename: str, filename_2: str = ""):
        result = None
        while result not in ["L", "R", "B"]:
            l_timestamp = datetime.fromtimestamp(os.stat(filename).st_mtime).strftime('%Y-%m-%d-%H:%M')
            r_timestamp = datetime.fromtimestamp(os.stat(filename_2).st_mtime).strftime('%Y-%m-%d-%H:%M')
            result = input(f"Duplicate file found: {filename} ({l_timestamp}) == {filename_2} ({r_timestamp})\n"
                  f"Choose which version you want to save: L - Left version, R - Right version, B - Both versions\n")
        if result == "L":
            return 0, None
        elif result == "R":
            return 1, None
        elif result == "B":
            return 2, True

    def clean(self, file_list, default_option=None):
        hash_table = {}
        for file in file_list:
            if os.stat(file).st_size != 0:
                fhash = hash_file(file)
                if fhash in hash_table.keys():
                    if default_option is None:
                        selected_option, default_option = self.prompt(file, hash_table[fhash])
                    else:
                        selected_option = default_option

                    if selected_option == 0:
                        os.remove(hash_table[fhash])
                        hash_table[fhash] = file
                    elif selected_option == 1:
                        os.remove(file)
                else:
                    hash_table[fhash] = file
        return hash_table


class EmptyFilesCleaner(CleanerModule):
    def prompt(self, filename: str, filename_2: str = ""):
        result = None
        while result not in ["R", "I", "RA", "IA"]:
            result = input(f"File \"{filename}\" is empty. R - Remove, I - Ignore, RA - Remove All, IA - Ignore All\n")
        if result == "R":
            return True, None
        elif result == "I":
            return False, None
        elif result == "RA":
            return True, True
        elif result == "IA":
            return False, False

    def clean(self, file_list, default_option=None):
        for file in file_list:
            if os.stat(file).st_size == 0:
                if default_option is None:
                    selected_option, default_option = self.prompt(file)
                else:
                    selected_option = default_option

                if selected_option:
                    os.remove(file)


class TempFilesCleaner(CleanerModule):
    def __init__(self, extension):
        self.extension = extension

    def prompt(self, filename: str, filename_2: str = ""):
        result = None
        while result not in ["R", "I", "RA", "IA"]:
            result = input(f"File \"{filename}\" is probably a temporary file. R - Remove, I - Ignore, "
                           f"RA - Remove All, IA - Ignore All\n")
        if result == "R":
            return True, None
        elif result == "I":
            return False, None
        elif result == "RA":
            return True, True
        elif result == "IA":
            return False, False

    def clean(self, file_list, default_option=None):
        for file in file_list:
            if fnmatch.fnmatch(file.split("/")[-1], self.extension):
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

    def prompt(self, filename: str, filename_2: str = ""):
        result = None
        while result not in ["Y", "N", "YA", "NO"]:
            result = input(f"Problematic character in filename: {filename}. Do you want to replace it? Y - Yes,"
                           f"N - No, YA - Yes for All, NO - No for All\n")
        if result == "Y":
            return True, None
        elif result == "N":
            return False, None
        elif result == "YA":
            return True, True
        elif result == "NO":
            return False, False

    def clean(self, file_list, default_option=None):
        for file in file_list:
            head, tail = os.path.split(file)
            for character in self.weird_characters:
                if character in tail:
                    if default_option is None:
                        temp_option, default_option = self.prompt(file)
                    else:
                        temp_option = default_option

                    if temp_option:
                        os.rename(file, os.path.join(head, tail.replace(character, self.replacement)))
