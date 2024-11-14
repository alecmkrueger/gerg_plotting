# filters.py

import numpy as np
import pandas as pd

def filter_var(var, min_value, max_value):
    var = var.where(var > min_value)
    var = var.where(var < max_value)
    return var

def filter_nan(values):
    return values[~np.isnan(values)]
