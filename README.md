### Introduction
This project is on-going project. Currently it goes on table features computation. We use DataFrame (supported by [Pandas](http://pandas.pydata.org)) as the main dataType for our data.

### Requirements
1. python 2.7
2. pandas >= 0.20.1
3. langdetect >= 1.0.7

### TODO
1. set up some test cases (travis)
2. merge some repeated computation? eg: in ```"num_distinct_tokens" (by fanghao)``` ```"most_common_tokens" (by ihui)``` both compute the Pandas Series of all tokens.
3. make it parallel computation

### Usage
use data_profile.py to profile the csv file into json format. Command line usage is as following:

```sh
python data_profile.py data.csv profiled_data.json
```

### Format
the output JSON format:

#### 1. columns format


```json
{
  "column_id": {
    "missing": {
        "num_missing": "the number of missing values (empty cells) in this column",
        "num_nonblank": "the number of non-blank(not NaN) cells in the column",
        "leading_space": "the number of leading whitespaces in the column",
        "trailing_space": "the number of trailing whitespaces in the column"
    },
    "special_type": {
    	"language": "language code, en, sp, etc.",
    	"num_filename": "number of cell that content might be a filename"
    },

    "length": {
      "character": {
        "average": "mean value of (number of chars in every cell)",
        "standard-deviation": "standard deviation of (number of chars in every cell)"
      },
      "token": {
        "average": "mean value of (number of chars for every token)",
        "standard-deviation": "standard deviation of (number of chars for every token)"
      }
    },
    "numeric_stats":{
        "integer": {
            "count": "the number of cells which are integers",
            "mean": "mean of integers in the column",
            "standard-deviation": "standard deviation of integers in the column",
            "Q1": "first quartile(25%) for integers in the column",
            "Q2": "second quartile(50%, median) for integers in the column",
            "Q3": "third quartile(75%) for integers in the column",
            "ratio": "ratio of integers in the column, #int divided by #non-blank",
            "num_positive":"number of positive integers in the column",
            "num_negative": "number of negative integers in the column",
            "num_1": "number of integer 1 in the column",
            "num_0": "number of integer 0 in the column",
            "num_-1":"number of integer -1 in the column",
            "num_outlier": "number of outliers n sigma away from mean, default n = 3, for integers"
        },
        "decimal": {
            "count": "the number of cell which are decimals, not include integer",
            "mean": "mean of decimals in the column",
            "standard-deviation": "standard deviation of decimals in the column",
            "Q1": "first quartile(25%) for decimals in the column",
            "Q2": "second quartile(50%, median) for decimals in the column",
            "Q3": "third quartile(75%) for decimals in the column",
            "ratio": "ratio of decimals in the column, #decimal divided by #non-blank",
            "num_positive":"number of positive decimals in the column",
            "num_negative": "number of negative decimals in the column",
            "num_1": "number of decimal 1.0 in the column",
            "num_0": "number of decimal 0.0 in the column",
            "num_-1":"number of decimal -1.0 in the column",
            "num_outlier": "number of outliers n sigma away from mean, default n = 3, for decimals"
        },
        "numeric": {
            "count": "number of numeric values in the column",
            "mean": "mean of numerical values in the column",
            "standard-deviation": "standard deviation of numerical values in the column",
            "Q1": "first quartile(25%) for numerical values in the column",
            "Q2": "second quartile(50%, median) for numerical values in the column",
            "Q3": "third quartile(75%) for numerical values in the column",
            "ratio": "ratio of numerical values in the column, #int divided by #non-blank",
            "num_positive":"number of positive values in the column",
            "num_negative": "number of negative values in the column",
            "num_1": "number of 1 and 1.0 in the column",
            "num_0": "number of 0 and 0.0 in the column",
            "num_-1":"number of -1 and -1.0 in the column",
            "num_outlier": "number of outliers n sigma away from mean, default n = 3",
        },
        "numeric_density": "density of Arabic numbers of the column",
        "contain_numeric": {
            "count": "number of cells which contain numeric character(s)",
            "ratio": "ratio of cells which contain numeric character(s)"
        },
        "contain_numeric_token": {
            "count": "number of tokens (default: split by space) which contain numeric character(s)",
            "ratio": "ratio of tokens (default: split by space) which contain numeric character(s)"
        },
        "contain_numeric_token_puncs": {
            "count": "number of tokens (split by string.punctuation) which contain numeric character(s)",
            "ratio": "ratio of tokens (split by string.punctuation) which contain numeric character(s)"
        },

    },
    "distinct":{
        "num_distinct_values": "the number of distinct values (consider the content in a cell as a value), ignore the missing value",
        "ratio_distinct_values": "num_distinct_values/num_rows, for num_rows, also ignore the missing value",
        "num_distinct_tokens": "same as num_distinct_values, but consider each token as a value, ignore the missing value",
        "ratio_distinct_tokens": "num_distinct_tokens/num_all_tokens, ignore the missing value",
        "num_distinct_tokens_puncs": "num of distinct tokens split by string.punctuation",
        "ratio_distinct_tokens_puncs":"ratio of distinct tokens split by string.punctuation"
    },

    "frequent-entries": {
      "most_common_values": {
          "value-1": "count 1",
          "value-2": "count-2",
          "value-k": "count-k"
      },
      "most_common_tokens": {
          "token-1": "count 1",
          "token-2": "count-2",
          "token-k": "count-k"
      },
      "most_common_tokens_puncs":{
          "token-1": "count 1",
          "token-2": "count-2",
          "token-k": "count-k"          
      },
      "most_common_punctuations": {
        "punctuation-1": {
        	"count": "number of occurrence of this punctuation in the whole column",
        	"density_of_all": "(count / number of all char in the column)",
        	"density_of_cell": "average of all cell: (count / number of all char in the cell)",
        	"num_outlier_cells": "number of outlier cells. Outlier cells is the cells that: density of puctuations in this cell is not within mean ± σ of the statics of the whole column"
        },
        "punctuation-2": {
        	"count": "number of occurrence of this punctuation in the whole column",
        	"density_of_all": "(count / number of all char in the column)",
        	"density_of_cell": "average of all cell: (count / number of all char in the cell)",
        	"num_outlier_cells": "number of outlier cells. Outlier cells is the cells that: density of puctuations in this cell is not within mean ± σ of the statics of the whole column"
        },
        "punctuation-k": {
        	"count": "number of occurrence of this punctuation in the whole column",
        	"density_of_all": "(count / number of all char in the column)",
        	"density_of_cell": "average of all cell: (count / number of all char in the cell)",
        	"num_outlier_cells": "number of outlier cells. Outlier cells is the cells that: density of puctuations in this cell is not within mean ± σ of the statics of the whole column"
        }
      },
      "most_common_alphanumeric_tokens": {
        "token-1": "count 1",
        "token-2": "count-2",
        "token-k": "count-4"
      },
      "most_common_numeric_tokens": {
        "token-1": "count 1",
        "token-2": "count-2",
        "token-k": "count-4"
      }
    }
  }
}
```

notes:

1. token: delimiter is a parameter (if set to ".", note that this will also be applied to floating numbers)
2. precision for floats: no round
3. punctuations does not apply for numbers (eg: for number 1.23, "." does not count as a punctuation)


#### 2. row format (TODO)
1. number of missing value
2. data type statistic: total count, ratio...
