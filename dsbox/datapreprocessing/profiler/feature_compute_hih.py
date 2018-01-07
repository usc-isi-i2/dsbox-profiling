import pandas as pd   # type: ignore
import numpy as np  # type: ignore
from . import helper_funcs as hf
from collections import OrderedDict
from collections import defaultdict
from collections import Counter
from builtins import filter

def ordered_dict2(column, k):
    unique,counts = np.unique(column, return_counts=True)
    d = dict(zip(unique,counts))
    dlist = []
    for k,v in Counter(d).most_common(k):
        e = {'name':k, 'count':v}
        dlist.append(e)
    return dlist

def ordered_dict(column, k):
    #d = column.value_counts()[:k].to_dict()
    d = column.value_counts().head(k).to_dict()
    dlist = []
    for k,v in sorted(d.items(), key=lambda x: x[1], reverse=True):
        e = {'name':k, 'count':v}
        dlist.append(e)
    return dlist

def tryConvert(cell):
    """
    convert a cell, if possible, to its supposed type(int, float, string)
    note: type of NaN cell is float
    """
    try:
        return int(cell)
    except ValueError as TypeError:
        try:
            return float(cell)
        except ValueError as TypeError:
            return cell

def numerical_stats(feature, column, num_nonblank, sigma=3):
    """
    calculates numerical statistics
    """
    stats = column.describe()
    feature['number_count'] = int(stats["count"])
    feature["number_ratio"] = stats["count"]/num_nonblank
    feature["number_mean"] = stats["mean"]
    feature["number_std"] = stats["std"]
    if stats["count"]==1: feature["number_std"]= 0
    feature["number_quartile_1"] = stats["25%"]
    feature["number_quartile_2"] = stats["50%"]
    feature["number_quartile_3"] = stats["75%"]
    outlier = column[(np.abs(column-stats["mean"])>(sigma*stats["std"]))]
    feature["number_outlier"] = outlier.count()
    feature["number_positive_count"] = column[column>0].count()
    feature["number_negative_count"] = column[column<0].count()
    feature["number_0"] = column[column==0].count()
    feature["number_1"] = column[column==1].count()
    feature["number_-1"] = column[column==-1].count()


def compute_numerics(column, feature):
    """
    computes numerical features of the column:
    # of integers/ decimal(float only)/ nonblank values in the column
    statistics of int/decimal/numerics
    """
    cnt = column.count()
    if column.dtype.kind in np.typecodes['AllInteger']+'uf' and cnt > 0:
        numerical_stats(feature, column, cnt)
    else:
        convert = lambda v: tryConvert(v)
        col = column.apply(convert, convert_dtype=False)

        col_nonblank = col.dropna()
        col_num = pd.Series([e for e in col_nonblank if type(e) == int or type(e) == np.int64 or type(e) == float or type(e) == np.float64])

        if col_num.count() > 0:
            numerical_stats(feature, col_num, cnt)

def compute_common_numeric_tokens(column, feature, k):
    """
    compute top k frequent numerical tokens and their counts.
    tokens are integer or floats
    e.g. "123", "12.3"
    """
    col = column.str.split(expand=True).unstack().dropna().values
    token = np.array(list(filter(lambda x: hf.is_Decimal_Number(x), col)))
    if token.size:
        feature["most_common_numeric_tokens"] = ordered_dict2(token, k)

def compute_common_alphanumeric_tokens(column, feature, k):
    """
    compute top k frequent alphanumerical tokens and their counts.
    tokens only contain alphabets and/or numbers, decimals with points not included
    """
    col = column.str.split(expand=True).unstack().dropna().values
    token = np.array(list(filter(lambda x: x.isalnum(), col)))
    if token.size:
        feature["most_common_alphanumeric_tokens"] = ordered_dict2(token, k)

def compute_common_values(column, feature, k):
    """
    compute top k frequent cell values and their counts.
    """
    if column.count() > 0:
        feature["most_common_values"] = ordered_dict(column, k)

def compute_common_tokens(column, feature, k):
    """
    compute top k frequent tokens and their counts.
    currently: tokens separated by white space
    at the same time, count on tokens which contain number(s)
    e.g. "$100", "60F", "123-456-7890"
    note: delimiter = " "
    """
    token = column.str.split(expand=True).unstack().dropna().values
    if token.size:
        feature["most_common_tokens"] = ordered_dict2(token, k)
        cnt = sum([any(char.isdigit() for char in c) for c in token])
        if cnt > 0:
            feature["contain_numeric_token_count"] = cnt
            feature["contain_numeric_token_ratio"] = float(cnt)/token.size

def compute_common_tokens_by_puncs(column, feature, k):
    """
    tokens seperated by all string.punctuation characters:
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    """
    col = column.dropna().values
    token_nested = [("".join((word if word.isalnum() else " ") for word in char).split()) for char in col]
    token = np.array([item for sublist in token_nested for item in sublist])
    if token.size:
        feature["most_common_tokens_split_by_punctuation"] = ordered_dict2(token, k)
        dist_cnt = np.unique(token).size
        feature["distinct_token_split_by_punctuation_count"] = dist_cnt
        feature["distinct_token_split_by_punctuation_ratio"] = float(dist_cnt)/token.size
        cnt = sum([any(char.isdigit() for char in c) for c in token])
        if cnt > 0:
            feature["contain_numeric_token_split_by_punctuation_count"] = cnt
            feature["contain_numeric_token_split_by_punctuation_ratio"] = float(cnt)/token.size

def compute_numeric_density(column, feature):
    """
    compute overall density of numeric characters in the column.
    """
    col = column.dropna().values
    if col.size:
        density = np.array([(sum(char.isdigit() for char in c), len(c)) for c in col])
        digit_total = density.sum(axis=0)
        feature["numeric_character_density"] = float(digit_total[0])/digit_total[1]

def compute_contain_numeric_values(column, feature):
    """
    caculate # and ratio of cells in the column which contains numbers.
    """
    contain_digits = lambda x: any(char.isdigit() for char in x)
    cnt = column.dropna().apply(contain_digits).sum()
    if cnt > 0:
        feature["contain_numeric_count"] = cnt
        feature["contain_numeric_ratio"] = float(cnt)/column.count()
