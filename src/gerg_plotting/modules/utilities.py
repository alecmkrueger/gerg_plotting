# utilities.py

import numpy as np
import pandas as pd
import datetime

def to_numpy_array(values):
    # convert set to list for pandas can convert to array
    if values is None:
        return None
    if isinstance(values,dict):
        values = values.values()
    if isinstance(values,set):
        values = list(values)
    if not isinstance(values, np.ndarray):
        array = pd.Series(values).to_numpy()
        return array
    elif isinstance(values, np.ndarray):
        return values
    else:
        raise ValueError(f"Cannot convert {type(values)} to a NumPy array")

def calculate_range(var):
    return [np.nanmin(var), np.nanmax(var)]

def calculate_pad(var, pad=0.0):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference * pad
    start = start - pad
    stop = stop + pad
    return float(start), float(stop)

def print_time(message):
    """
    Prints a message with the current time in 'HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%H:%M:%S')}")

def print_datetime(message):
    """
    Prints a message with the current date and time in 'YYYY-MM-DD HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
