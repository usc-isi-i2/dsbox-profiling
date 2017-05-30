import pandas as pd
import json
import sys

# from feature computation functions
import feature_compute_lfh
import feature_compute_hih

"""
Main function to profile the data.
"""

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

    for column_name in data:
        each_res = {} # dict: map feature name to content
        feature_compute_lfh.compute_length(data[column_name], each_res)
        feature_compute_lfh.compute_missing(data[column_name], each_res)

        feature_compute_hih.compute_numerics(data[column_name], each_res)
        feature_compute_hih.compute_numeric_tokens(data[column_name], each_res)
        feature_compute_hih.compute_alphanumeric_tokens(data[column_name], each_res)

        result[column_name] = each_res # add this column features into final result

    print "====================calculations finished ====================\n"
    # STEP 3: wirting JSON formated output
    print "     ====================>> wirting to file: {}\n".format(output_filename)
    output_json = json.dumps(result)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print  "======================ALL DONE ===================="
