import hashlib
import glob
import shutil
import os


""" 
    Copy Files to new flat folder and remove duplication using hash function. Also, 
    slipt to many subfolder for easy to upload to cloud
 
    Call Funtion:
    main(
        r"source folder",
        r"destination folder",
        "MOV",
        "SHA1",
        10000,
        1000_000_000,
    )
"""


def make_hash(filename, hashtype):
    hashtype = hashtype.upper()
    BLOCKSIZE = 65536

    if hashtype == "MD5":
        hasher = hashlib.md5()
    elif hashtype == "SHA1":
        hasher = hashlib.sha1()
    elif hashtype == "SHA256":
        hasher = hashlib.sha256()

    with open(filename, "rb") as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def main(
    source_path,
    destination_path,
    file_type,
    hash_type="SHA1",
    min_size=1_000_000,
    max_size=10_000_000,
    selected_mode="l",
    number_of_folders=1,
):
    os.chdir(destination_path)
    file_type_ = "." + file_type.lower()

    file_list = glob.glob(f"{source_path}/**/*{file_type_}", recursive=True)
    total_file_list = len(file_list)

    mode = selected_mode  # input("Enter Mode(l list, c copy, s split): ")
    folder_to_create = number_of_folders  # int(input("Enter # of Folders (1-10): "))

    for i, old_file in enumerate(file_list):
        # print(f" Assigned folder: {assigned_folder} file: {i+1} ")

        file_size = os.stat(old_file).st_size
        file_running_number = i + 1
        pct = file_running_number / total_file_list

        old_name = os.path.basename(old_file).replace(file_type_, "")
        old_filename, old_extension = os.path.splitext(old_file)
        # old_extension = old_extension.replace(".", "")
        hash_text = make_hash(filename=old_file, hashtype=hash_type)
        short_hash_text = hash_text[0:7]

        if min_size < file_size < max_size:
            # print(file_size)

            if mode == "l":
                mode_flag = "List"
                new_file = ("_n_" + short_hash_text + file_type_).upper()
                new_full_path = destination_path + "\\" + new_file
                print(
                    f"{mode_flag} File#: {file_running_number:<5} | {pct:<6.0%} of {total_file_list:>6} | {hash_type:>}: {hash_text[0:7]} | New: {new_file:>} | Old: {old_name:<40} | Size: {file_size:>12,}"
                )

            elif mode == "c":
                mode_flag = "Copy"
                new_file = ("_n_" + short_hash_text + old_extension).upper()
                new_full_path = destination_path + "\\" + new_file
                # Copy file only
                try:
                    shutil.copy(old_file, new_full_path)
                except:
                    print(f"File: {new_file} already exists. Skip it")

                print(
                    f"{mode_flag} File#: {file_running_number:<5} | {pct:<6.0%} of {total_file_list:>6} | {hash_type:>}: {hash_text[0:7]} | New: {new_file:>} | Old: {old_name:<40} | Size: {file_size:>12,}"
                )

            elif mode == "s":
                mode_flag = "Split"
                assigned_folder = (i % folder_to_create) + 1
                width = 3
                assigned_folder = str(assigned_folder).rjust(
                    width, "0"
                )  # add three zero
                new_file = (
                    str(assigned_folder) + "\\" + "_n_" + short_hash_text + file_type_
                ).upper()  # with folder as prefix
                new_full_path = destination_path + "\\" + new_file
                # Create Folders
                for f in range(folder_to_create):
                    new_folder = destination_path + "\\" + str(f + 1)
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                try:
                    # shutil.copy(old_file, new_full_path)
                    shutil.move(old_file, new_full_path)
                except:
                    print(f"File: {new_file} already exists. Skip it")

                print(
                    f"{mode_flag} Folder: {assigned_folder} File#: {file_running_number:<5} | {pct:<6.0%} of {total_file_list:>6} | {hash_type:>}: {hash_text[0:7]} | New: {new_file:>} | Old: {old_name:<40} | Size: {file_size:>12,}"
                )


if __name__ == "__main__":
    pass
