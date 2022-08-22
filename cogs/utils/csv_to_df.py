import pathlib

import numpy as np
import pandas as pd
from cogs.utils.file_exists import get_filepaths
from cogs.utils.file_exists import get_raw_string
from cogs.utils.file_exists import list_to_string


def csv_to_df_to_dict(path):
    csv_ = pathlib.Path(path)

    csv_ = get_raw_string(list_to_string(get_filepaths(csv_)))

    with open(csv_, "rb", buffering=0) as f:
        data_frame = pd.read_csv(f)

        data_frame = data_frame.replace(r"^\s*$", np.NaN, regex=True)  #

        data_frame = data_frame.dropna(thresh=2, axis=1)

        data_frame = data_frame.drop(["GMT", "PHST", "PST"], axis=1)

        data_frame_1 = data_frame.melt("EST").dropna(subset=["value"])
        return {k: dict(zip(v["EST"], v["value"])) for k, v in data_frame_1.groupby("variable")}
