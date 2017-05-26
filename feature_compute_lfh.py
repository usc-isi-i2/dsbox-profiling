import pandas as pd
import helper_funcs

def compute_missing(column, feature):
    """
    compute the number of missing value for a given series (column); store the result into (feature)
    """
    feature["num_missing"] = pd.isnull(column).sum()


def compute_length(column, feature):
    """
    compute the mean and std for a given series (column); 
    mean and std precision: 5 after point
    missing value (NaN): treated as does not exist
    """
    column = column.dropna() # get rid of all missing value
    
    feature["length"] = {} # for character and token
    # 1. for character
    feature["length"]["character"] = {}
    lenth_for_all =  column.apply(len)
    feature["length"]["character"]["average"] = '{0:.5g}'.format(lenth_for_all.mean())
    feature["length"]["character"]["standard-deviation"] = '{0:.5g}'.format(lenth_for_all.std())
    
    # 2. for token
    feature["length"]["token"] = {}
    tokenlized = column.str.split()    # default: tokenlize by blank space (can be a hyper-parameter)
    flatten_list = pd.Series([])
    for i in tokenlized:
        flatten_list = flatten_list.append(pd.Series(i), ignore_index = True)
    
    lenth_for_token = flatten_list.apply(len)
    feature["length"]["token"]["average"] = '{0:.5g}'.format(lenth_for_token.mean())
    feature["length"]["token"]["standard-deviation"] = '{0:.5g}'.format(lenth_for_token.std())