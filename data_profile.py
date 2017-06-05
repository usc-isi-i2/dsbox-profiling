import pandas as pd
import json
import sys

# from feature computation functions
import feature_compute_lfh
import feature_compute_hih

def profile_data(data_path, output_filename):
    """
    Main function to profile the data.
    """
    # hyper-parameters
    punctuation_outlier_weight = 2;
    token_delimiter = " ";

    # STEP 1: get dependency and read data
    data = pd.read_csv(data_path, dtype = object)   # all read as str
    print "====================have a look on the data: ====================\n"
    print data.head()

    # STEP 2: calculations
    print "====================calculating the features ... ====================\n"
    result = {} # final result: dict of dict

    for column_name in data:
        each_res = {} # dict: map feature name to content
        feature_compute_lfh.compute_length_distinct(data[column_name], each_res, delimiter=token_delimiter)
        feature_compute_lfh.compute_missing(data[column_name], each_res)
        feature_compute_lfh.compute_lang(data[column_name], each_res)
        feature_compute_lfh.compute_punctuation(data[column_name], each_res, weight_outlier=punctuation_outlier_weight)

        feature_compute_hih.compute_numerics(data[column_name], each_res)
        feature_compute_hih.compute_common_numeric_tokens(data[column_name], each_res)
        feature_compute_hih.compute_common_alphanumeric_tokens(data[column_name], each_res)
        feature_compute_hih.compute_common_values(data[column_name], each_res)
        feature_compute_hih.compute_common_tokens(data[column_name], each_res)
        feature_compute_hih.compute_numeric_density(data[column_name], each_res)

        result[column_name] = each_res # add this column features into final result

    print "====================calculations finished ====================\n"
    # STEP 3: wirting JSON formated output
    print "     ====================>> wirting to file: {}\n".format(output_filename)
    output_json = json.dumps(result, indent=4)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print  "======================ALL DONE ===================="


if __name__ == '__main__':
    """
    main function to execute profiler
    """
    profile_data(sys.argv[1], sys.argv[2])
