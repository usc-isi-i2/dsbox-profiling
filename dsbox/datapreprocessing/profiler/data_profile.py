import pandas as pd
import json
import sys
import time
import numpy as np

# from feature computation functions
import feature_compute_lfh as fc_lfh
import feature_compute_hih as fc_hih
from collections import defaultdict


class Profiler(object):
    """
    data profiler moduel. Now only supports csv data.

    Parameters:
    ----------
    punctuation_outlier_weight: a integer
        the coefficient used in outlier detection for punctuation. default is 3 

    numerical_outlier_weight

    token_delimiter: a string
        delimiter that used to seperate tokens, default is blank space " ".

    detect_language: boolean
        true: do detect language; false: not detect language

    topk: a integer
    

    verbose: boolean
        control the verbose 

    Attributes:
    ----------
    
    """

    def __init__(self, punctuation_outlier_weight=3, 
        numerical_outlier_weight=3, token_delimiter=" ", 
        detect_language=False, topk=10, verbose=False):
        self.punctuation_outlier_weight = punctuation_outlier_weight
        self.numerical_outlier_weight = numerical_outlier_weight
        self.token_delimiter = token_delimiter
        self.detect_language = detect_language
        self.topk = topk
        self.verbose = verbose




    def profile_data(self, data_path):

        """
        Main function to profile the data.
        Parameters
        ----------
        data_path: file or pandas DataFrame that needs to be profiled
        ----------
        """
        # STEP 1: get dependency and read data

        isDF = False
        ## csv as input ##
        if not isinstance(data_path, pd.DataFrame):
            data = pd.read_csv(data_path, dtype = object)   # all read as str
            data_for_corr = pd.read_csv(data_path)
            corr_pearson = data_for_corr.corr()
            corr_spearman = data_for_corr.corr(method='spearman')

        ## data frame as imput ##
        else:
            data = data_path
            isDF = True
            corr_pearson = data.corr()
            corr_spearman = data.corr(method='spearman')

        corr_columns = list(corr_pearson.columns)

        if self.verbose:
            print("====================have a look on the data: ====================\n")
            print(data.head())

        # STEP 2: calculations
        if self.verbose: 
            print("====================calculating the features ... ====================\n")
        result = {} # final result: dict of dict
        for column_name in data:
            col = data[column_name]
            # dict: map feature name to content
            each_res = defaultdict(lambda: defaultdict())

            if column_name in corr_columns:
                corr_dict = {}
                corr_dict["columns"] = corr_columns
                corr_dict["pearson"] = list(corr_pearson[column_name])
                corr_dict["spearman"] = list(corr_spearman[column_name])

                each_res["numeric_stats"]["correlation"] = corr_dict

            if col.dtype.kind in np.typecodes['AllInteger']+'uMmf':
                each_res["missing"]["num_missing"] = pd.isnull(col).sum()
                each_res["missing"]["num_nonblank"] = col.count()
                each_res["special_type"]["dtype"] = str(col.dtype)
                ndistinct = col.nunique()
                each_res["distinct"]["num_distinct_values"] = ndistinct
                each_res["distinct"]["ratio_distinct_values"] = ndistinct/ float(col.size)

            if col.dtype.kind == 'b':
                each_res["special_type"]["data_type"] = 'bool'
                fc_hih.compute_common_values(col.dropna().astype(str), each_res, self.topk)

            elif col.dtype.kind in np.typecodes['AllInteger']+'u':
                each_res["special_type"]["data_type"] = 'integer'
                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_values(col.dropna().astype(str), each_res,self.topk)

            elif col.dtype.kind == 'f':
                each_res["special_type"]["data_type"] = "float"
                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_values(col.dropna().astype(str), each_res,self.topk)

            elif col.dtype.kind == 'M':
                each_res["special_type"]["data_type"] = "datetime"

            elif col.dtype.kind == 'm':
                each_res["special_type"]["data_type"] = "timedelta"

            else:
                if isDF:
                    if col.dtype.name == 'category':
                        each_res["special_type"]["data_type"] = 'category'
                    col = col.astype(object).fillna('').astype(str)

                # compute_missing_space Must be put as the first one because it may change the data content, see function def for details
                fc_lfh.compute_missing_space(col, each_res)
                fc_lfh.compute_filename(col, each_res)
                fc_lfh.compute_length_distinct(col, each_res, delimiter=self.token_delimiter)
                if self.detect_language: fc_lfh.compute_lang(col, each_res)
                fc_lfh.compute_punctuation(col, each_res, weight_outlier=self.punctuation_outlier_weight)

                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_numeric_tokens(col, each_res,self.topk)
                fc_hih.compute_common_alphanumeric_tokens(col, each_res, self.topk)
                fc_hih.compute_common_values(col, each_res, self.topk)
                fc_hih.compute_common_tokens(col, each_res, self.topk)
                fc_hih.compute_numeric_density(col, each_res)
                fc_hih.compute_contain_numeric_values(col, each_res)
                fc_hih.compute_common_tokens_by_puncs(col, each_res, self.topk)

            if not each_res["numeric_stats"]: del each_res["numeric_stats"]

            result[column_name] = each_res # add this column features into final result

        if self.verbose: print("====================calculations finished ====================\n")

        return result

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

if __name__ == '__main__':
    """
    main function to execute profiler
    """
    profiler = Profiler()
    result = profiler.profile_data(sys.argv[1])
    output_filename = sys.argv[2]
    # wirting JSON formated output
    print("     ====================>> wirting to file: {}\n".format(output_filename))
    output_json = json.dumps(result, indent=4, cls=MyEncoder)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print ("======================ALL DONE ====================")
