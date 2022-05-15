import os
import fnmatch


def scan_files(root):  # listdir
    all_files = []
    walk = [root]
    while walk:
        folder = walk.pop(0) + "/"
        items = os.listdir(folder)
        for i in items:
            i = folder + i
            (walk if os.path.isdir(i) else all_files).append(i)
    return all_files


def ask_empty(file):
    result = None
    while result not in ["R", "I", "RA", "IA"]:
        result = input(f"File \"{file}\" is empty. R - Remove, I - Ignore, RA - Remove All, IA - Ignore All\n")
    if result == "R":
        return True, None
    elif result == "I":
        return False, None
    elif result == "RA":
        return True, True
    elif result == "IA":
        return False, False


def ask_temp(file):
    result = None
    while result not in ["R", "I", "RA", "IA"]:
        result = input(f"File \"{file}\" is probably a temporary file. R - Remove, I - Ignore, RA - Remove All, "
                       f"IA - Ignore All\n")
    if result == "R":
        return True, None
    elif result == "I":
        return False, None
    elif result == "RA":
        return True, True
    elif result == "IA":
        return False, False


def rm_empty_files(file_list, save_option=None):
    modified_file_list = []
    for file in file_list:
        if os.stat(file).st_size == 0:
            if save_option is None:
                temp_option, save_option = ask_empty(file)
            else:
                temp_option = save_option

            if temp_option:
                os.remove(file)
            else:
                modified_file_list.append(file)
        else:
            modified_file_list.append(file)
    return modified_file_list.copy()


def rm_temp_files(file_list, temp_regex, save_option=None):
    modified_file_list = []
    for file in file_list:
        if fnmatch.fnmatch(file.split("/")[-1], temp_regex):
            if save_option is None:
                temp_option, save_option = ask_temp(file)
            else:
                temp_option = save_option

            if temp_option:
                os.remove(file)
            else:
                modified_file_list.append(file)
        else:
            modified_file_list.append(file)
    return modified_file_list.copy()
