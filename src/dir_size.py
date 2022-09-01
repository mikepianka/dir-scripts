import os
import time
from typing import Union


def human_bytes(B: Union[int, float]) -> str:
    """Return the provided bytes as a human readable string.

    :param B: numeric bytes
    :type B: Union[int, float]
    :return: B, KB, MB, GB, or TB string
    :rtype: str
    """

    B = float(B)
    KB = float(1024)
    MB = float(KB**2)  # 1,048,576
    GB = float(KB**3)  # 1,073,741,824
    TB = float(KB**4)  # 1,099,511,627,776

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)


def total_tree_size(top_dir: str) -> str:
    """Find the total size of a directory tree on disk.

    :param top_dir: the directory to begin the search from
    :type top_dir: str
    :return: comma separated string of the directory and its size on disk in bytes
    :rtype: str
    """

    total_size = 0

    for dirpath, dirnames, filenames in os.walk(top_dir):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(filepath):
                try:
                    total_size += os.path.getsize(filepath)
                except FileNotFoundError:
                    # likely a Windows path that is too long, add extended-length path prefix
                    filepath_extended = "\\\\?\\" + filepath
                    total_size += os.path.getsize(filepath_extended)

    print(top_dir + " total size is " + human_bytes(total_size))

    size_string = f'"{top_dir}",{total_size}'
    return size_string


def each_tree_size(top_dir: str) -> str:
    """Find the total size on disk of each child directory tree within the provided top level directory.

    :param top_dir: the directory to begin the search from
    :type top_dir: str
    :return: path to the output log file
    :rtype: str
    """

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    log_file_path = os.path.join(top_dir, f"directory_total_sizes_{timestamp}.txt")

    top_dir_items = os.listdir(top_dir)

    dir_paths = [
        os.path.join(top_dir, item)
        for item in top_dir_items
        if os.path.isdir(os.path.join(top_dir, item))
    ]

    print(f"Found {len(dir_paths)} dirs in {top_dir}. Calculating sizes...")

    for count, dir_path in enumerate(dir_paths, start=1):
        print(f"Examining dir {count} of {len(dir_paths)}...")

        size_string = total_tree_size(dir_path)

        with open(log_file_path, "a") as log_file:
            log_file.write(size_string + "\n")

    print(f"Finished! A log of the results can be found in {log_file_path}")
    return log_file_path


if __name__ == "__main__":
    print(
        "This script will find the total size on disk of each child directory tree within "
        + "the top level directory you provide."
    )

    while True:
        start_dir = input("Enter the directory path to start evaluating from: ")
        if os.path.exists(start_dir) and os.path.isdir(start_dir):
            break
        else:
            print(
                "Directory path does not exist or was not typed correctly; enter again..."
            )

    each_tree_size(start_dir)
