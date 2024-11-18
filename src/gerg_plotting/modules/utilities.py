# utilities.py

import numpy as np
import pandas as pd
import datetime


def to_numpy_array(values) -> np.ndarray:
    # convert set to list for pandas can convert to numpy array

    # Early return if values is None
    if values is None:
        return None
    # Return early if values are already a numpy array
    elif isinstance(values, np.ndarray):
        return values
    if isinstance(values,dict):
        raise TypeError(f"Cannot convert a dict with values of '{values}' to a NumPy array")
    # Convert set to list before attempting to convert
    elif isinstance(values,set):
        values = list(values)
    # Try to convert to numpy using pandas series as the parser
    array = pd.Series(values).to_numpy()
    return array


def calculate_range(var) -> list[float,float]:
    return [np.nanmin(var), np.nanmax(var)]


def calculate_pad(var, pad=0.0) -> tuple[float,float]:
    start, stop = calculate_range(var)
    start_with_pad = start - pad
    stop_with_pad = stop + pad
    return float(start_with_pad), float(stop_with_pad)


def print_time(message) -> None:
    """
    Prints a message with the current time in 'HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%H:%M:%S')}")


def print_datetime(message) -> None:
    """
    Prints a message with the current date and time in 'YYYY-MM-DD HH:MM:SS' format.

    Parameters:
        message (str): The message to include in the output.
    """
    print(f"{message}: {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
