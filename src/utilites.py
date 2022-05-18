import hashlib
import os

HASH_BUFFER = 65536


def scan_files(root):
    all_files = []
    walk = [root]
    while walk:
        folder = walk.pop(0) + "/"
        items = os.listdir(folder)
        for i in items:
            i = folder + i
            (walk if os.path.isdir(i) else all_files).append(i)
    return all_files


def hash_from_file(filename):
    sha = hashlib.sha512()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(HASH_BUFFER)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()
