### Introduction
This project is on-going project. Currently it goes on table features computation. We use DataFrame (supported by [Pandas](http://pandas.pydata.org)) as the main dataType for our data.

### Requirements
1. python 2.7
2. pandas >= 0.20.1

### TODO
1. set up some test cases
2. merge some repeated computation? eg: in ```"num_distinct_tokens" (by fanghao)``` ```"most_common_tokens" (by ihui)``` both compute the Pandas Series of all tokens.

### Usage
use data_profile.py to profile the csv file into json format. Command line usage is as following:

```sh
python data_profile.py data.csv profiled_data.json
```

### Format
the output JSON format:

1. columns format


```json
{
  "column_id": {
    "num_missing": "the number of missing values (empty cells) in this column",
    "language": "language code, en, sp, etc.",
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
    "num_integer": "the number of cell that it contains integer",
    "num_decimal": "the number of cell that it contains decimal",
    "integer": {
        "mean": "mean of integers in the column",
        "standard-deviation": "standard deviation of integers in the column",
        "Q1": "first quartile(25%) of integers in the column",
        "Q2": "second quartile(50%, median) of integers in the column",
        "Q3": "third quartile(75%) of integers in the column",
        "ratio": "ratio of integers in the column, #int divided by #non-blank"
    },
    "decimal": {
        "mean": "mean of integers in the column",
        "standard-deviation": "standard deviation of decimals in the column",
        "Q1": "first quartile(25%) of decimals in the column",
        "Q2": "second quartile(50%, median) of decimals in the column",
        "Q3": "third quartile(75%) of decimals in the column",
        "ratio": "ratio of decimals in the column, #int divided by #non-blank"
    },
    "numeric": {
        "mean": "mean of numerical values in the column",
        "standard-deviation": "standard deviation of integers in the column",
        "Q1": "first quartile(25%) of integers in the column",
        "Q2": "second quartile(50%, median) of integers in the column",
        "Q3": "third quartile(75%) of integers in the column",
        "ratio": "ratio of integers in the column, #int divided by #non-blank"
    },
    "numeric_density": "density of arabic numbers of the column",
    "num_distinct_values": "the number of distinct values (consider the content in a cell as a value), ignore the missing value",
    "ratio_distinct_values": "num_distinct_values/num_rows, for num_rows, also ignore the missing value",
    "num_distinct_tokens": "same as num_distinct_values, but consider each token as a value, ignore the missing value",
    "ratio_distinct_tokens": "num_distinct_tokens/num_all_tokens, ignore the missing value",
    "frequent-entries": {
      "most_common_values": {
        "value-1": "count 1",
        "value-2": "count-2",
        "value-k": "count-4"
      },
      "most_common_tokens": {
        "token-1": "count 1",
        "token-2": "count-2",
        "token-k": "count-4"
      },
      "most_common_punctuations": {
        "punctuation-1": {
        	"count": "number of occurrence of this punctuation in the whole column",
        	"density_of_all": "(count / number of all char in the column)",
        	"density_of_cell": "average of all cell: (count / number of all char in the cell)",
        	"num_outlier_cells": "number of outlier cells. Outlier cells is the cells that: density of puctuations in this cell is not within mean ± σ of the statics of the whole column"
        }
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
2. precision for floats: 5 after point
3. punctuations does not apply for numbers (eg: for number 1.23, "." does not count as a punctuation)


