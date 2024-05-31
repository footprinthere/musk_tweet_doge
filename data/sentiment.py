from enum import Enum

import numpy as np
import pandas as pd


class ColumnName(str, Enum):
    AVERAGE = "average"
    WEIGHTED_AVERAGE = "weighted_average"
    N_POSITIVE = "n_positive"
    N_NEGATIVE = "n_negative"
    N_TOTAL = "n_total"

    BULLISHNESS = "bullishness"
    POSITIVE_RATIO = "positive_ratio"
    NEGATIVE_RATIO = "negative_ratio"
    CUMULATED_POSITIVE_RATIO = "cumulated_positive_ratio"
    CUMULATED_NEGATIVE_RATIO = "cumulated_negative_ratio"


def add_bullishness(data: pd.DataFrame) -> pd.DataFrame:
    # bullishness = log((1+n_pos) / (1+n_neg))
    data[ColumnName.BULLISHNESS] = np.log(
        (1 + data[ColumnName.N_POSITIVE]) / (1 + data[ColumnName.N_NEGATIVE])
    )
    return data


def add_ratio(data: pd.DataFrame) -> pd.DataFrame:
    # ratio = {n_pos or n_neg} / n_total
    data[ColumnName.POSITIVE_RATIO] = (
        data[ColumnName.N_POSITIVE] / data[ColumnName.N_TOTAL]
    )
    data[ColumnName.NEGATIVE_RATIO] = (
        data[ColumnName.N_NEGATIVE] / data[ColumnName.N_TOTAL]
    )

    # cumulated ratio : ratio calculated from the first row to the current row
    data[ColumnName.CUMULATED_POSITIVE_RATIO] = (
        data[ColumnName.N_POSITIVE].cumsum() / data[ColumnName.N_TOTAL].cumsum()
    )
    data[ColumnName.CUMULATED_NEGATIVE_RATIO] = (
        data[ColumnName.N_NEGATIVE].cumsum() / data[ColumnName.N_TOTAL].cumsum()
    )

    return data


def add_diff(data: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    """diff = value[t] - value[t]"""
    diff_format = "diff_{}"
    for column_name in column_names:
        data[diff_format.format(column_name)] = data[column_name].diff()
        # value of the first row will be NaN
    return data


def add_log_diff(data: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    """log_diff = log(value[t] / value[t-1])"""
    log_diff_format = "log_diff_{}"
    for column_name in column_names:
        data[log_diff_format.format(column_name)] = np.log(
            data[column_name] / data[column_name].shift(1)
        )
        # value of the first row will be NaN
    return data
