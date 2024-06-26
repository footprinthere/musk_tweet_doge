from typing import Optional

import numpy as np
import pandas as pd
from eventstudy import Single


def single_import_returns(
    data: pd.DataFrame,
    is_price: bool,
    log_return: bool,
    date_format: Optional[str] = "%Y-%m-%dT%H:%M:%S",
):
    """
    `date_format`: Set `None` if the date is already in datetime format.
    """

    if date_format is not None:
        data["date"] = pd.to_datetime(data["date"], format=date_format)

    if not is_price:
        Single._save_parameter("returns", data)
        return

    converted_data = data.iloc[1:]  # remove the first row
    for key in data.keys():
        if key != "date":
            if log_return:
                converted_data.loc[:, key] = np.diff(np.log(data[key]))
            else:
                converted_data.loc[:, key] = np.diff(data[key]) / data[key][1:]

    Single._save_parameter("returns", converted_data)
