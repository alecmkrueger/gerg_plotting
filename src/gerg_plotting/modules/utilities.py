# utilities.py

import numpy as np
import pandas as pd

def to_numpy_array(values):
    # convert set to list for pandas can convert to array
    if isinstance(values,dict):
        values = values.values()
    if isinstance(values,set):
        values = list(values)
    if not isinstance(values, np.ndarray):
        array = pd.Series(values).to_numpy()
        return array
    elif isinstance(values, np.ndarray):
        return values
    elif values is None:
        return None
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

def print_time(value=None, intervals=[10, 50, 100, 500, 1000]):
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if value is None:
        print(current_time)
        return
    if not len(intervals) >= 2:
        raise ValueError(f'Not enough intervals, need at least 2 values, you passed {len(intervals)}')
    if value <= intervals[0]:
        print(f'{value = }, {current_time}')
    elif value <= intervals[-2]:
        for idx, interval in enumerate(intervals[:-1]):
            if interval <= value < intervals[idx+1] and value % interval == 0:
                print(f'{value = }, {current_time}')
    elif value >= intervals[-1] and value % intervals[-1] == 0:
        print(f'{value = }, {current_time}')
