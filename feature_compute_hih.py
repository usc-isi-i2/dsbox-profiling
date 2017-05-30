import pandas as pd
import numpy as np

def tryConvert(cell):
    """
    convert a cell, if possible, to its supposed type(int, float, string)
    note: type of NaN cell is float
    """
    try:
        return int(cell)
    except ValueError, TypeError:
        try:
            return float(cell)
        except ValueError, TypeError:
            return cell

def numerical_stats(column,num_nonblank):
    """
    calculates numerical statistics
    decimal: 5 after point
    """
    stats = column.describe().apply(lambda x: round(x,5))
    idict = {}
    idict["mean"] = stats["mean"]
    idict["standard-deviation"] = stats["std"]
    idict["Q1"] = stats["25%"]
    idict["Q2"] = stats["50%"]
    idict["Q3"] = stats["75%"]
    idict["ratio"] = round(stats["count"]/num_nonblank,5)
    return idict

def compute_numerics(column, feature):
    """
    computes numerical features of the column:
    # of integers/ decimal(float only)/ nonblank values in the column
    statistics of int/decimal/numerics
    """
    convert = lambda v: tryConvert(v)
    col = column.apply(convert)
    #col = pd.to_numeric(column,errors='ignore') #doesn't work in messy column?

    col_nonblank = col.dropna()
    col_int = pd.Series([e for e in col_nonblank if type(e) == int or type(e) == np.int64])
    col_float = pd.Series([e for e in col_nonblank if type(e) == float or type(e) == np.float64])

    feature["num_integer"] = col_int.count()
    feature["num_decimal"] = col_float.count() # not include integers
    feature["num_nonblank"] = col_nonblank.count()

    if feature["num_integer"] > 0:
        feature["integer"] = numerical_stats(col_int,feature["num_nonblank"])

    if feature["num_decimal"] > 0:
        feature["decimal"] = numerical_stats(col_float,feature["num_nonblank"])

    if "integer" in feature or "decimal" in feature:
        feature["numerics"] = numerical_stats(pd.concat([col_float,col_int]),feature["num_nonblank"])
