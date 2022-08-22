from __future__ import annotations

import copy
import io
import re
from typing import Any

import dateparser
from cogs.utils.csv_to_df import csv_to_df_to_dict
from cogs.utils.lists_dicts import order
from cogs.utils.paths_for_functions import path_for_csv_to_dict

temp_value = ""
temp_string_containing_time = ""


def get_days() -> list:
    """Gets the list of days in the dict and then sorts them"""
    days = [key for key in csv_to_df_to_dict(path_for_csv_to_dict)]
    days.sort(key=order.index)
    return days


def get_timezone_for_date_parser() -> str:
    day = get_days()[0]
    first_key = next(iter(csv_to_df_to_dict(path_for_csv_to_dict)[day]))
    first_key = str(first_key)
    first_key = str(first_key.split("(")[1].split(")")[0])
    return " " + first_key


x = get_timezone_for_date_parser()


def get_string_for_time() -> str:
    """Stores in a multiline string the various times for the events.
    These times are in a datetime form. For example: 2021-02-26 08:30:00-05:00
    """
    global temp_value
    string_for_time = ""
    for day in get_days():
        for key, value in csv_to_df_to_dict(path_for_csv_to_dict)[day].items():
            if "Eastern" in key:
                temp_value = str(value)
            if "Eastern" not in key:
                key = "".join((temp_value, "Time ", key))
                if "Time" in key:
                    temp_list = re.sub(r"(\d{1,2}:\d{2}):", r"\g<1>", key)
                    key = "".join(temp_list)
                if "Time" in key:
                    temp_list = key.split("Time")
                    key = "".join(temp_list)
                    key += x
                    string_for_time += str(dateparser.parse(key))
                    string_for_time += "\n"
    return string_for_time


def get_deep_copy(dict_to_copy: dict) -> dict:
    """Returns a deep copy of the dict passed in"""
    return copy.deepcopy(dict_to_copy)


def get_starting_string(string_file_to_read: str) -> str:
    """Gets the first string in a file"""
    with io.StringIO(string_file_to_read) as f:
        temp_string = f.readline()
        return temp_string.rstrip("\n")


def next_string(string_file_to_read: str, string_to_compare: str) -> Any | None:
    """Compares a string to a text file and gets the next string in the file"""
    with io.StringIO(string_file_to_read) as f:
        temp_string = f.readline()
        temp_string = temp_string.rstrip("\n")
        if temp_string == string_to_compare:  # fix new line here
            next_ = next(f)
            return next_.rstrip("\n")
        else:
            while string_to_compare != temp_string:
                temp_string = f.readline()
                temp_string = temp_string.rstrip("\n")
            try:
                if string_to_compare == temp_string:
                    next_ = next(f)
                    return next_.rstrip("\n")
                else:
                    raise StopIteration("Expected positive integer")
            except StopIteration:
                return


def modify_dict(dict_to_modify: dict) -> dict:
    """Takes a dict and modifies it so that it's times are in the datetime form( 2021-02-26 08:30:00-05:00 )"""
    global temp_string_containing_time
    count = 0
    for day in get_days():
        if count < 1:
            temp_string_containing_time = get_starting_string(get_string_for_time())
            count += 1
        for key in csv_to_df_to_dict(path_for_csv_to_dict)[day].copy():
            if "Eastern" not in key:
                dict_to_modify.copy()[day][temp_string_containing_time] = dict_to_modify.copy()[day].pop(key)
                temp_string_containing_time = next_string(get_string_for_time(), temp_string_containing_time)
    return dict_to_modify
