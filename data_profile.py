import pandas as pd
import json
import sys
import time

# from feature computation functions
import feature_compute_lfh
import feature_compute_hih
from collections import defaultdict

def profile_data(data_path):
    """
    Main function to profile the data.
    Parameters
    ----------
    data_path: file that needs to be profiled
    ----------
    """
    # hyper-parameters
    punctuation_outlier_weight = 3;
    numerical_outlier_weight = 3;
    token_delimiter = " ";
    detect_language = False;

    # STEP 1: get dependency and read data
    data = pd.read_csv(data_path, dtype = object)   # all read as str
    print "====================have a look on the data: ====================\n"
    print data.head()

    # STEP 2: calculations
    print "====================calculating the features ... ====================\n"
    result = {} # final result: dict of dict
    for column_name in data:
        #each_res = {} # dict: map feature name to content
        each_res = defaultdict(lambda: defaultdict())
        # compute_missing_space Must be put as the first one because it may change the data content, see function def for details
        feature_compute_lfh.compute_missing_space(data[column_name], each_res)
        feature_compute_lfh.compute_filename(data[column_name], each_res)    
        feature_compute_lfh.compute_length_distinct(data[column_name], each_res, delimiter=token_delimiter)
        if detect_language: feature_compute_lfh.compute_lang(data[column_name], each_res)
        feature_compute_lfh.compute_punctuation(data[column_name], each_res, weight_outlier=punctuation_outlier_weight)

        feature_compute_hih.compute_numerics(data[column_name], each_res)
        feature_compute_hih.compute_common_numeric_tokens(data[column_name], each_res)
        feature_compute_hih.compute_common_alphanumeric_tokens(data[column_name], each_res)
        feature_compute_hih.compute_common_values(data[column_name], each_res)
        feature_compute_hih.compute_common_tokens(data[column_name], each_res)
        feature_compute_hih.compute_numeric_density(data[column_name], each_res)
        feature_compute_hih.compute_contain_numeric_values(data[column_name], each_res)
        feature_compute_hih.compute_common_tokens_by_puncs(data[column_name], each_res)
        if not each_res["numeric_stats"]: del each_res["numeric_stats"]

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

