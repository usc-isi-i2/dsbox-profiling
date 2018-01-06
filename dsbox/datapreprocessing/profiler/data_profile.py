import pandas as pd  # type: ignore
import json
import sys
import time
import numpy as np  # type: ignore
import typing


# from feature computation functions
from . import feature_compute_lfh as fc_lfh
from . import feature_compute_hih as fc_hih
from collections import defaultdict

from primitive_interfaces.transformer import TransformerPrimitiveBase
from d3m_metadata import container, hyperparams, metadata
from d3m_metadata.container import dataset

Input = typing.Union[container.Dataset, \
                    container.DataFrame]
# Input = container.DataFrame
Output = container.Dataset

class Hyperparams(hyperparams.Hyperparams):
    """
    No hyper-parameters for this primitive.
    """

    pass

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
    __author__ = 'USC ISI'
    __version__ = '0.2.0'
    metadata = metadata.PrimitiveMetadata({
            'id': 'b2612849-39e4-33ce-bfda-24f3e2cb1e93',
            'version': __version__,
            'name': "Profiler",
            'keywords': ['profiler'],
            'source': {
                'name': __author__,
                'uris': [
                    # Unstructured URIs. Link to file and link to repo in this case.
                    'https://github.com/usc-isi-i2/dsbox-profiling/blob/master/dsbox/datapreprocessing/profiler/data_profile.py',
                    'https://github.com/usc-isi-i2/dsbox-profiling.git',
                    ],
            },
            # The same path the primitive is registered with entry points in setup.py.
            'installation': [{
                'type': metadata.PrimitiveInstallationType.PIP,
                'package_uri': 'https://github.com/usc-isi-i2/dsbox-profiling.git'
            }],
            'python_path': 'd3m.primitives.dsbox.profiler',
            # Choose these from a controlled vocabulary in the schema. If anything is missing which would
            # best describe the primitive, make a merge request.

            'algorithm_types': [
                metadata.PrimitiveAlgorithmType.DATA_PROFILING,
            ],
            'primitive_family': metadata.PrimitiveFamily.DATA_PREPROCESSING,
            # A metafeature about preconditions required for this primitive to operate well.

            # for profiler, maybe no precon
            "precondition": []
        })
    
    
    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, 
            docker_containers: typing.Union[typing.Dict[str, str], None] = None) -> None:
        # All primitives must define these attributes
        self.hyperparams = hyperparams
        self.random_seed = random_seed
        self.docker_containers = docker_containers

        # All other attributes must be private with leading underscore  
        self._punctuation_outlier_weight = 3
        self._numerical_outlier_weight = 3
        self._token_delimiter = " "
        self._detect_language = False
        self._topk = 10
        self._verbose = hyperparams['verbose'] if hyperparams else 0



    def produce(self, *, inputs: Input, timeout: float = None, iterations: int = None) -> Output:
        if isinstance(inputs, dataset.Dataset):
            # perhaps multiple tables
            # return self._profile_data(inputs)
            self.results = inputs.metadata
            for table_id in inputs:
                dataframe = pd.DataFrame(data = inputs[table_id])
                print (dataframe)
                self._profile_data(dataframe, table_id)    # inplace manipulate

            inputs.metadata = self.results
            return inputs
        else:
            # single table
            key = "0" # default key for single table
            self.results = metadata.Metadata()
            self._profile_data(inputs, key)
 
            
            ds = dataset.Dataset({key: inputs}, self.results)
            return ds
            

    def _profile_data(self, data_path, table_id="0"):

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

        if self._verbose:
            print("====================have a look on the data: ====================\n")
            print(data.head())

        # STEP 2: calculations
        if self._verbose:
            print("====================calculating the features ... ====================\n")
        result = {} # final result: dict of dict
        column_counter = -1
        for column_name in data:
            column_counter += 1
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
                each_res["missing_value_count"] = pd.isnull(col).sum()
                each_res["non_missing_value_count"] = col.count()
                each_res["special_type"]["dtype"] = str(col.dtype)
                ndistinct = col.nunique()
                each_res["distinct_value_count"] = ndistinct
                each_res["distinct_value_ratio"] = ndistinct/ float(col.size)

            if col.dtype.kind == 'b':
                each_res["special_type"]["data_type"] = 'bool'
                fc_hih.compute_common_values(col.dropna().astype(str), each_res, self._topk)

            elif col.dtype.kind in np.typecodes['AllInteger']+'u':
                each_res["special_type"]["data_type"] = 'integer'
                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_values(col.dropna().astype(str), each_res,self._topk)

            elif col.dtype.kind == 'f':
                each_res["special_type"]["data_type"] = "float"
                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_values(col.dropna().astype(str), each_res,self._topk)

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
                # fc_lfh.compute_filename(col, each_res)
                fc_lfh.compute_length_distinct(col, each_res, delimiter=self._token_delimiter)
                if self._detect_language: fc_lfh.compute_lang(col, each_res)
                fc_lfh.compute_punctuation(col, each_res, weight_outlier=self._punctuation_outlier_weight)

                fc_hih.compute_numerics(col, each_res)
                fc_hih.compute_common_numeric_tokens(col, each_res,self._topk)
                fc_hih.compute_common_alphanumeric_tokens(col, each_res, self._topk)
                fc_hih.compute_common_values(col, each_res, self._topk)
                fc_hih.compute_common_tokens(col, each_res, self._topk)
                fc_hih.compute_numeric_density(col, each_res)
                fc_hih.compute_contain_numeric_values(col, each_res)
                fc_hih.compute_common_tokens_by_puncs(col, each_res, self._topk)

            if not each_res["numeric_stats"]: del each_res["numeric_stats"]

            # result[column_name] = each_res # add this column features into final result

            self.results = self.results.update((table_id, metadata.ALL_ELEMENTS, column_counter,), each_res)

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
