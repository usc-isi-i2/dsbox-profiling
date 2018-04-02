import pandas as pd  # type: ignore
import json
import sys
import time
import numpy as np  # type: ignore
import typing

# from feature computation functions
from . import feature_compute_lfh as fc_lfh
from . import feature_compute_hih as fc_hih
from . import category_detection
from . import config
from collections import defaultdict

from d3m.primitive_interfaces.transformer import TransformerPrimitiveBase
from d3m import container, metadata
from d3m.container import dataset
from d3m.metadata import hyperparams, base

Input = typing.Union[container.Dataset, \
                    container.DataFrame]
# Input = container.DataFrame
Output = container.Dataset

VERBOSE = 0

computable_metafeatures = ['ratio_of_values_containing_numeric_char', 'ratio_of_numeric_values', 
    'number_of_outlier_numeric_values', 'num_filename', 'number_of_tokens_containing_numeric_char', 
    'number_of_numeric_values_equal_-1', 'most_common_numeric_tokens', 'most_common_tokens', 
    'ratio_of_distinct_tokens', 'number_of_missing_values', 
    'number_of_distinct_tokens_split_by_punctuation', 'number_of_distinct_tokens', 
    'ratio_of_missing_values', 'semantic_types', 'number_of_numeric_values_equal_0', 
    'number_of_positive_numeric_values', 'most_common_alphanumeric_tokens', 
    'numeric_char_density', 'ratio_of_distinct_values', 'number_of_negative_numeric_values', 
    'target_values', 'ratio_of_tokens_split_by_punctuation_containing_numeric_char', 
    'ratio_of_values_with_leading_spaces', 'number_of_values_with_trailing_spaces', 
    'ratio_of_values_with_trailing_spaces', 'number_of_numeric_values_equal_1', 
    'natural_language_of_feature', 'most_common_punctuations', 'spearman_correlation_of_features', 
    'number_of_values_with_leading_spaces', 'ratio_of_tokens_containing_numeric_char', 
    'number_of_tokens_split_by_punctuation_containing_numeric_char', 'number_of_numeric_values', 
    'ratio_of_distinct_tokens_split_by_punctuation', 'number_of_values_containing_numeric_char', 
    'most_common_tokens_split_by_punctuation', 'number_of_distinct_values', 
    'pearson_correlation_of_features']

default_metafeatures = ['ratio_of_values_containing_numeric_char', 'ratio_of_numeric_values', 
    'number_of_outlier_numeric_values', 'num_filename', 'number_of_tokens_containing_numeric_char']

class Hyperparams(hyperparams.Hyperparams):
    features = hyperparams.EnumerationList(values = computable_metafeatures, 
        default = default_metafeatures, 
        semantic_types=['https://metadata.datadrivendiscovery.org/types/DataMetafeatures'])
    


class Profiler(TransformerPrimitiveBase[Input, Output, Hyperparams]):
    """
    data profiler moduel. Now only supports csv data.

    Parameters:
    ----------
    _punctuation_outlier_weight: a integer
        the coefficient used in outlier detection for punctuation. default is 3

    _numerical_outlier_weight

    _token_delimiter: a string
        delimiter that used to seperate tokens, default is blank space " ".

    _detect_language: boolean
        true: do detect language; false: not detect language

    _topk: a integer


    _verbose: boolean
        control the _verbose

    Attributes:
    ----------

    """
    metadata = hyperparams.base.PrimitiveMetadata({
        'id': 'b2612849-39e4-33ce-bfda-24f3e2cb1e93',
        'version': config.VERSION, 
        'name': "DSBox Profiler",
        'description': 'Generate profiles of datasets',
        'python_path': 'd3m.primitives.dsbox.Profiler',
        'primitive_family': base.PrimitiveFamily.DATA_PREPROCESSING,
        'algorithm_types': [
            base.PrimitiveAlgorithmType.DATA_PROFILING,
        ],
        'keywords': ['data_profiler'],
        'source': {
            'name': config.D3M_PERFORMER_TEAM,
            'uris': [ config.REPOSITORY ],
        },
            # The same path the primitive is registered with entry points in setup.py.
        'installation': [ config.INSTALLATION ],
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.

        # A metafeature about preconditions required for this primitive to operate well.
        "precondition": [],
        "hyperparms_to_tune": []
    })
    
    
    def __init__(self, *, hyperparams: Hyperparams) -> None:
        super().__init__(hyperparams=hyperparams)

        # All other attributes must be private with leading underscore  
        self._punctuation_outlier_weight = 3
        self._numerical_outlier_weight = 3
        self._token_delimiter = " "
        self._detect_language = False
        self._topk = 10
        self._verbose = VERBOSE
        # list of specified features to compute
        self._specified_features = hyperparams['features'] if hyperparams else default_metafeatures



    def produce(self, *, inputs: Input, timeout: float = None, iterations: int = None) -> Output:
        """
        generate features for the input. 

        Input:
            dataset.Dataset or DataFrame
        Output:
            dataset.Dataset


        """
        if isinstance(inputs, dataset.Dataset):
            # perhaps multiple tables
            self.results = inputs.metadata # store metadata as a class-level variable
            for table_id in inputs:
                dataframe = pd.DataFrame(data = inputs[table_id])
                self._profile_data(dataframe, table_id)    # inplace manipulate metadata

            inputs.metadata = self.results
            return inputs
        else:
            # single table
            key = "0" # default key for single table
            self.results = metadata.Metadata() # store metadata as a class-level variable
            
            self._profile_data(inputs, table_id=key)
            
            ds = dataset.Dataset({key: inputs}, self.results)
            return ds
            

    def _profile_data(self, data, table_id="0"):

        """
        Main function to profile the data. This functions will 
        1. calculate features
        2. put them in self.results

        Parameters
        ----------
        data: pandas.DataFrame that needs to be profiled
        ----------
        """
        if self._verbose:
            print("====================have a look on the data: ====================\n")
            print(data.head())

        # calculations
        if self._verbose:
            print("====================calculating the features ... ====================\n")

        # STEP 1: data-level calculations
        if ("pearson_correlation_of_features" in self._specified_features):
            corr_pearson = data.corr()
            corr_columns = list(corr_pearson.columns)
            corr_id = [data.columns.get_loc(n) for n in corr_columns]

        if ("spearman_correlation_of_features" in self._specified_features):
            corr_spearman = data.corr(method='spearman')
            corr_columns = list(corr_spearman.columns)
            corr_id = [data.columns.get_loc(n) for n in corr_columns]
        
        is_category = category_detection.category_detect(data)

        # STEP 2: column-level calculations
        column_counter = -1
        for column_name in data:
            column_counter += 1
            col = data[column_name]
            # dict: map feature name to content
            each_res = defaultdict(lambda: defaultdict())
            
            if is_category[column_name]:
                each_res['semantic_types'] = ["https://metadata.datadrivendiscovery.org/types/CategoricalData"]
            
            if (("spearman_correlation_of_features" in self._specified_features) and 
                (column_name in corr_columns) ):
                stats_sp = corr_spearman[column_name].describe()
                each_res["spearman_correlation_of_features"] = {'min': stats_sp['min'],
                                                                'max': stats_sp['max'],
                                                                'mean': stats_sp['mean'],
                                                                'median': stats_sp['50%'],
                                                                'std': stats_sp['std']}
            
            if (("spearman_correlation_of_features" in self._specified_features) and 
                (column_name in corr_columns) ):
                stats_pr = corr_pearson[column_name].describe()
                each_res["pearson_correlation_of_features"] = {'min': stats_pr['min'],
                                                                'max': stats_pr['max'],
                                                                'mean': stats_pr['mean'],
                                                                'median': stats_pr['50%'],
                                                                'std': stats_pr['std']}

            if col.dtype.kind in np.typecodes['AllInteger']+'uMmf':
                if ("number_of_missing_values" in self._specified_features):
                    each_res["number_of_missing_values"] = pd.isnull(col).sum()
                if ("ratio_of_missing_values" in self._specified_features):
                    each_res["ratio_of_missing_values"] = pd.isnull(col).sum() / col.size
                if ("number_of_distinct_values" in self._specified_features):   
                    each_res["number_of_distinct_values"] = col.nunique()
                if ("ratio_of_distinct_values" in self._specified_features):
                    each_res["ratio_of_distinct_values"] = col.nunique() / float(col.size)

            if col.dtype.kind == 'b':
                if ("most_common_raw_values" in self._specified_features):
                    fc_hih.compute_common_values(col.dropna().astype(str), each_res, self._topk)

            elif col.dtype.kind in np.typecodes['AllInteger']+'uf':
                fc_hih.compute_numerics(col, each_res) # TODO: do the checks inside the function
                if ("most_common_raw_values" in self._specified_features):
                    fc_hih.compute_common_values(col.dropna().astype(str), each_res,self._topk)

            else:
                col = col.astype(object).fillna('').astype(str)

                # compute_missing_space Must be put as the first one because it may change the data content, see function def for details
                fc_lfh.compute_missing_space(col, each_res, self._specified_features)
                # fc_lfh.compute_filename(col, each_res)
                fc_lfh.compute_length_distinct(col, each_res, delimiter=self._token_delimiter, feature_list=self._specified_features)
                if ("natural_language_of_feature" in self._specified_features): 
                    fc_lfh.compute_lang(col, each_res)
                if ("most_common_punctuations" in self._specified_features):
                    fc_lfh.compute_punctuation(col, each_res, weight_outlier=self._punctuation_outlier_weight)

                fc_hih.compute_numerics(col, each_res, self._specified_features)
                if ("most_common_numeric_tokens" in self._specified_features):
                    fc_hih.compute_common_numeric_tokens(col, each_res,self._topk)
                if ("most_common_alphanumeric_tokens" in self._specified_features):
                    fc_hih.compute_common_alphanumeric_tokens(col, each_res, self._topk)
                if ("most_common_raw_values" in self._specified_features):
                    fc_hih.compute_common_values(col, each_res, self._topk)
                fc_hih.compute_common_tokens(col, each_res, self._topk, self._specified_features)
                if ("numeric_char_density" in self._specified_features):
                    fc_hih.compute_numeric_density(col, each_res)
                fc_hih.compute_contain_numeric_values(col, each_res, self._specified_features)
                fc_hih.compute_common_tokens_by_puncs(col, each_res, self._topk, self._specified_features)

            # update metadata for a specific column
            self.results = self.results.update((table_id, metadata.base.ALL_ELEMENTS, column_counter,), each_res)

        if self._verbose: print("====================calculations finished ====================\n")


        return self.results

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
    result = profiler._profile_data(sys.argv[1])
    output_filename = sys.argv[2]
    # wirting JSON formated output
    print("     ====================>> wirting to file: {}\n".format(output_filename))
    output_json = json.dumps(result, indent=4, cls=MyEncoder)
    f = open(output_filename, 'w')
    f.write(output_json)
    f.close()
    print ("======================ALL DONE ====================")
