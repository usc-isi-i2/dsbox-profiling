import pandas as pd
import json
import sys
import time
import numpy as np

# from feature computation functions
import feature_compute_lfh as fc_lfh
import feature_compute_hih as fc_hih
from collections import defaultdict

def profile_data(data_path, punctuation_outlier_weight=3, 
        numerical_outlier_weight=3, token_delimiter=" ", detect_language=False, topk=10):
    """
    Main function to profile the data.
    Parameters
    ----------
    data_path: file or pandas DataFrame that needs to be profiled
    ----------
    """
    ## hyper-parameters
    #punctuation_outlier_weight = 3;
    #numerical_outlier_weight = 3;
    #token_delimiter = " ";
    #detect_language = False;

    # STEP 1: get dependency and read data
    
    isDF = False
    ## csv as input ##
    if not isinstance(data_path, pd.DataFrame):
        data = pd.read_csv(data_path, dtype = object)   # all read as str
    
    ## data frame as imput ##
    else:
        data = data_path
        isDF = True
    
    print "====================have a look on the data: ====================\n"
    print data.head()

    # STEP 2: calculations
    
    print "====================calculating the features ... ====================\n"
    result = {} # final result: dict of dict
    for column_name in data:
        col = data[column_name]
        # dict: map feature name to content
        each_res = defaultdict(lambda: defaultdict())

        if col.dtype == np.float:
            ##num_missing?for NaN=float
            each_res["special_type"]["dtype"] = "float"
            fc_hih.compute_numerics(col, each_res)
            fc_hih.compute_common_values(col.dropna().astype(str), each_res,topk)
        elif col.dtype == np.integer:
            ##probably no missing?
            each_res["special_type"]["dtype"] = "integer"
            fc_hih.compute_numerics(col, each_res)
            fc_hih.compute_common_values(col.dropna().astype(str), each_res,topk)
        elif col.dtype == 'datetime64[ns]':
            each_res["special_type"]["dtype"] = "datetime64[ns]"
        elif col.dtype == 'timedelta64[ns]':
            each_res["special_type"]["dtype"] = "timedelta64[ns]"
        elif col.dtype == bool:
            ##probably no missing?
            each_res["missing"]["num_nonblank"] = col.count()
            each_res["special_type"]["dtype"] = "bool"
            fc_hih.compute_common_values(col.dropna().astype(str), each_res, topk)
        elif col.dtype == object:
            if isDF:
                col = col.fillna('').astype(str)
            # compute_missing_space Must be put as the first one because it may change the data content, see function def for details
            fc_lfh.compute_missing_space(col, each_res)
            fc_lfh.compute_filename(col, each_res)    
            fc_lfh.compute_length_distinct(col, each_res, delimiter=token_delimiter)
            if detect_language: fc_lfh.compute_lang(col, each_res)
            fc_lfh.compute_punctuation(col, each_res, weight_outlier=punctuation_outlier_weight)

            fc_hih.compute_numerics(col, each_res)
            fc_hih.compute_common_numeric_tokens(col, each_res,topk)
            fc_hih.compute_common_alphanumeric_tokens(col, each_res, topk)
            fc_hih.compute_common_values(col, each_res, topk)
            fc_hih.compute_common_tokens(col, each_res, topk)
            fc_hih.compute_numeric_density(col, each_res)
            fc_hih.compute_contain_numeric_values(col, each_res)
            fc_hih.compute_common_tokens_by_puncs(col, each_res, topk)
            if not each_res["numeric_stats"]: del each_res["numeric_stats"]
        else:
            print "cannot recoginze dtype of the column, please make it some recognizable dtype first."

        result[column_name] = each_res # add this column features into final result

    print "====================calculations finished ====================\n"

    return result
    

if __name__ == '__main__':
    """
    main function to execute profiler
    """
    result = profile_data(sys.argv[1])
    output_filename = sys.argv[2]
    # wirting JSON formated output
    print "     ====================>> wirting to file: {}\n".format(output_filename)
    output_json = json.dumps(result, indent=4)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print  "======================ALL DONE ===================="

