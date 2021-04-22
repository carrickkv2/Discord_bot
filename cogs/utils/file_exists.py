import datetime
import os.path
import pathlib
import typing
import shutil
import random
from cogs.utils.paths_for_functions import path_for_file_exists_file_path, path_for_file_exists_shuntil

filepath = pathlib.Path(path_for_file_exists_file_path)
new_destination = pathlib.Path()


def get_filepaths(directory: typing.Union[str, bytes, os.PathLike]) -> list:
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


_dRawMap = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}


# Run the above function and store its results in a variable.
def list_to_string(list_: list) -> str:
    """Turns a list into a string"""
    return ''.join(list_)


def get_raw_string(s: str) -> str:
    """Takes a filepath string and turns it into a raw string"""
    return r''.join(_dRawMap.get(ord(c), c) for c in s)


full_file_paths = get_filepaths(filepath)
full_file_paths = list_to_string(full_file_paths)
full_file_paths = get_raw_string(full_file_paths)

# print(get_raw_string(full_file_paths))
# file_path = os.path.basename(full_file_paths)

# Get the current time and parse it into a human readable format.
utc_time = datetime.datetime.utcnow()
utc_time = utc_time.strftime("%a %b %d %Y %I %M %p")


def rename_and_move(filepath: typing.Union[str, bytes, os.PathLike]) -> None:
    """Renames the file in a directory and then moves it"""
    for dirpath, dirnames, files in os.walk(filepath):
        if files:
            try:
                rand = random.SystemRandom()
                rand = str(rand.randint(0, 10000))
                rand += " "
                # print(dirpath, 'has files')  # rename the file
                new = str(dirpath + '\\' + utc_time + rand + '.csv')
                os.rename(full_file_paths, get_raw_string(new))
                path_to_move = get_raw_string(list_to_string(get_filepaths(filepath)))
                shutil.move(path_to_move, path_for_file_exists_shuntil)
            except Exception as e:
                print(e)
                raise


def rename_csv(filepath: typing.Union[str, bytes, os.PathLike]) -> None:
    """Renames the csv given"""
    for dirpath, dirnames, files in os.walk(filepath):
        if files:
            try:
                # print(dirpath, 'has no files')  # rename the file
                new = str(dirpath + '\\' + 'table' + '.csv')
                os.rename(get_raw_string(list_to_string(get_filepaths(filepath))), get_raw_string(new))
            except Exception as e:
                print(e)
                raise

# move old to another folder totally?
# has file: rename and then move else return.
# Todo: refactor and loop through rename and move so that we can rename more than one file
