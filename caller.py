import os
from remove_dups import main
import time

# 2021 Done MP4:383 MOV:326
# File Type: MOV MP4


def list_files(source, destination, file_type, min_size, max_size):
    main(
        source,
        destination,
        file_type,
        "SHA1",
        min_size,
        max_size,
        "l",
        1,
    )


def copy_files(source, destination, file_type, min_size, max_size):
    main(
        source,
        destination,
        file_type,
        "SHA1",
        min_size,
        max_size,
        "c",
        1,
    )


def split_files(source, file_type, min_size, max_size, folder):
    main(
        source,
        source,
        file_type,
        "SHA1",
        min_size,
        max_size,
        "s",
        folder,
    )


def start_small():
    min_size = 1_000_000
    max_size = 10_000_000
    start_program(min_size, max_size)


def start_medium():
    min_size = 10_000_000
    max_size = 100_000_000
    start_program(min_size, max_size)


def start_large():
    min_size = 100_000_000
    max_size = 10_000_000_000
    start_program(min_size, max_size)


def start_program(min_size, max_size):
    print()
    source = r"C:\Users\vsayakanit\OneDrive - Pittsburgh Water and Sewer Authority\Pictures\Camera Roll\2022"
    print(source)
    output = r"C:\Users\vsayakanit\OneDrive - Pittsburgh Water and Sewer Authority\Temp_Delete_Any_Time"
    print(output)
    # file_type = ["MP4"]
    file_type = ["M??"]  # using wildcard ??
    # file_type = ["MP4", "MOV", "AVI", "MPG", "MKV", "WMV", "WebM"]
    print(f"File Extension: {file_type}")
    min_size = 1_000_000
    print(f"File Min Size: {min_size:,}")
    max_size = 10_000_000
    print(f"File Max Size: {max_size:,}")
    print()
    mode = input("Enter Mode(l list, c copy, s split, f count files): ")
    print()

    for ext in file_type:
        print("-" * 140)
        print(f"File Type: {ext}")
        if mode == "l":
            list_files(source, output, ext, min_size, max_size)
        elif mode == "c":
            start = time.time()
            copy_files(source, output, ext, min_size, max_size)
            end = time.time()
            elapsed_time = end - start
            print(f"Time: {elapsed_time}")
        elif mode == "s":
            number_of_folder = int(input("Enter Folder (1-99): "))
            split_files(output, ext, min_size, max_size, number_of_folder)
        elif mode == "f":
            path = output
            # limit = 100
            print()

            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    file_count = len(os.listdir(dir_path))
                    print(f"{dir} has {file_count} files.")


if __name__ == "__main__":
    while True:
        start_small()
        # start_medium
        # start_large()
