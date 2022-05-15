import os
import random

from cleaner import scan_files


def make_mess():
    random.seed(2137)
    os.system('./make_mess.sh')
    for file in scan_files("X"):
        if random.randint(1, 10) == 1:
            os.remove(file)
    for file in scan_files("Y1"):
        if random.randint(1, 10) == 1:
            os.remove(file)
        elif random.randint(1, 10) == 2:
            head, tail = os.path.split(file)
            os.rename(file, os.path.join(head, tail+"_mod"))
    for file in scan_files("Y2"):
        if random.randint(1, 10) == 1:
            os.remove(file)
        elif random.randint(1, 10) == 2:
            head, tail = os.path.split(file)
            os.rename(file, os.path.join(head, tail+"_mod"))


if __name__ == '__main__':
    make_mess()
