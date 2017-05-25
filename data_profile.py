import pandas as pd
import helper_funcs
import json
import sys

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


if __name__ == '__main__':
    # STEP 1: get dependency and read data 
    data_path = sys.argv[1]
    output_filename = sys.argv[2]
    # if not specify dtype, it will read in some format: like int
    data = pd.read_csv(data_path, dtype = object) 
    print "====================have a look on the data: ====================\n"
    print data.head()

    # STEP 2: calculations
    print "====================calculating the features ... ====================\n"
    result = {} # final result: dict of dict

    for column in data:
        each_res = {} # dict: map feature name to content
        compute_length(data[column], each_res)
        
        result[column] = each_res # add this column features into final result

    print "====================calculations finished ====================\n"
    # STEP 3: wirting JSON formated output
    print "     ====================>> wirting to file: {}\n".format(output_filename)
    output_json = json.dumps(result)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print  "======================ALL DONE ===================="