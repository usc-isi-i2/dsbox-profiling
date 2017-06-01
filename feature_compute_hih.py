import pandas as pd
import numpy as np
import helper_funcs as hf
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
        feature["numeric"] = numerical_stats(pd.concat([col_float,col_int]),feature["num_nonblank"])

def compute_common_numeric_tokens(column, feature, k=10):
    """
    compute top k frequent numerical tokens and their counts.
    tokens are integer or floats
    """
    #num_split = lambda x: filter(lambda y: unicode(y).isnumeric(),x.split())    
    num_split = lambda x: filter(lambda y: hf.is_Decimal_Number(y), x.split())
    token = column.dropna().apply(num_split).apply(pd.Series).unstack().dropna()
    if token.count() > 0:
        if ("frequent-entries" not in feature.keys()):
            feature["frequent-entries"] = {}
        feature["frequent-entries"]["most_common_numeric_tokens"] = token.value_counts()[:k].to_dict()

def compute_common_alphanumeric_tokens(column, feature, k=10):
    """
    compute top k frequent alphanumerical tokens and their counts.
    tokens only contain alphabets and/or numbers, decimals with points not included 
    """
    alnum_split = lambda x: filter(lambda y: y.isalnum(),x.split())
    token = column.dropna().apply(alnum_split).apply(pd.Series).unstack().dropna()
    if token.count() > 0:
        if ("frequent-entries" not in feature.keys()):
            feature["frequent-entries"] = {}
        feature["frequent-entries"]["most_common_alphanumeric_tokens"] = token.value_counts()[:k].to_dict()

def compute_common_values(column, feature, k=10):
    """
    compute top k frequent cell values and their counts.
    """
    if column.count() > 0:
        if ("frequent-entries" not in feature.keys()):
            feature["frequent-entries"] = {}
        feature["frequent-entries"]["most_common_values"] = column.value_counts()[:k].to_dict()

def compute_common_tokens(column, feature, k=10):
    """
    compute top k frequent tokens and their counts.
    currently: tokens separated by white space
    """
    token = column.dropna().apply(lambda x: x.split()).apply(pd.Series).unstack()
    if token.count() > 0:
        if ("frequent-entries" not in feature.keys()):
            feature["frequent-entries"] = {}
        feature["frequent-entries"]["most_common_tokens"] = token.value_counts()[:k].to_dict()

def compute_numeric_density(column, feature):
    """
    compute overall density of numeric characters in the column.
    """
    density = lambda x: (sum(c.isdigit() for c in x),len(x))
    digit_total = column.dropna().apply(density).apply(pd.Series).sum()
    feature["numeric_density"] = round(float(digit_total[0])/digit_total[1], 5)
