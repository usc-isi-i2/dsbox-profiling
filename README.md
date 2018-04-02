[![Build Status](https://travis-ci.org/usc-isi-i2/dsbox-profiling.svg?branch=master)](https://travis-ci.org/usc-isi-i2/dsbox-profiling)

### Introduction
A TA1 primitives for [d3m](https://gitlab.com/datadrivendiscovery/d3m) project Currently it generates data
profiles for tabular data. We use DataFrame (supported by
[Pandas](http://pandas.pydata.org)) as our main data type.

### Requirements
see [setup.py](./setup.py)




### Installation

1. install [d3m](https://gitlab.com/datadrivendiscovery/d3m) project first.


2. use pip:

```shell
pip install dsbox-dataprofiling
```
	
### Usage
see [example.py](./example.py)

you can chose the metafeautures based on what you need. Our computable metafeatures including:

```
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
```

for the specific meaning and data structure of the metafeature, you can lookup this page: [data_metafeatures](https://gitlab.com/datadrivendiscovery/d3m/blob/devel/d3m/metadata/schemas/v0/definitions.json#L63)

