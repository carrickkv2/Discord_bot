import csv
import pathlib
from cogs.utils.lists_dicts import new_file_headers
from cogs.utils.paths_for_functions import path_for_csv_to_dict
from cogs.utils.file_exists import get_raw_string, get_filepaths, list_to_string


def write_csv(r_string: str) -> None:
    """
    Takes the csv outputted by extract_to_csv and rewrites it so that it can be used by the cogs.
    """
    table = pathlib.Path(r_string)

    with open(table, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        with open(get_raw_string(list_to_string(get_filepaths(path_for_csv_to_dict))), 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)

            csv_writer.writerow(new_file_headers)

            for line in reader:
                csv_writer.writerow(line)
