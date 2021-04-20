import pandas as pd
import numpy as np
import pathlib
from cogs.utils.file_exists import get_raw_string, get_filepaths, list_to_string


def csv_to_df_to_dict(path):
    csv_ = pathlib.Path(path)
    # r'G:\Python-Projects\Pip\Discord Test\Discord Bot\csv'
    csv_ = get_raw_string(list_to_string(get_filepaths(csv_)))

    with open(csv_, "rb", buffering=0) as f:
        data_frame = pd.read_csv(f)

        # data_frame = pd.read_csv(csv_)  # Read the csv and store in df
        data_frame = data_frame.replace(r'^\s*$', np.NaN, regex=True)  # Replace all empty strings with NaN.
        # Empty strings can't be used to determine if a column should be dropped.

        data_frame = data_frame.dropna(thresh=2, axis=1)  # Drop a column if the NaN values are greater 2

        data_frame = data_frame.drop(['GMT', 'PHST', 'PST'], axis=1)  # Drop the timezones we don't need

        data_frame_1 = data_frame.melt('EST').dropna(subset=['value'])
        return {k: dict(zip(v['EST'], v['value'])) for k, v in data_frame_1.groupby('variable')}



