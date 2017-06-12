[![Build Status](https://travis-ci.org/usc-isi-i2/dsbox-cleaning.svg?branch=master)](https://travis-ci.org/usc-isi-i2/dsbox-cleaning)

### Introduction
This project is an on-going project. Currently it generates data
profiles for tabular data. We use DataFrame (supported by
[Pandas](http://pandas.pydata.org)) as our main data type.

### Requirements
1. python 2.7
2. pandas >= 0.20.1
3. langdetect >= 1.0.7

### TODO
1. merge some repeated computation? eg: in ```"num_distinct_tokens" (by fanghao)``` ```"most_common_tokens" (by ihui)``` both compute the Pandas Series of all tokens.
2. perform parallel computation

### Usage
To profile a csv data file, do:

```
from dsbox.datapreprocessing.profiler import profile_data
jsonResult = profile_data('data.csv')
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

### Sample output

See examples directory for more sample outputs.

```json
{
    "stoptm": {
        "ratio_distinct_tokens": 0.24483, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "1800.0": 27, 
                "800.0": 36, 
                "1300.0": 24, 
                "1000.0": 37, 
                "1600.0": 26, 
                "2100.0": 25, 
                "1700.0": 24, 
                "900.0": 28, 
                "1900.0": 28, 
                "700.0": 25
            }, 
            "most_common_values": {
                "1800.0": 27, 
                "800.0": 36, 
                "1300.0": 24, 
                "1000.0": 37, 
                "1600.0": 26, 
                "2100.0": 25, 
                "1700.0": 24, 
                "900.0": 28, 
                "1900.0": 28, 
                "700.0": 25
            }, 
            "most_common_tokens": {
                "1800.0": 27, 
                "800.0": 36, 
                "1300.0": 24, 
                "1000.0": 37, 
                "1600.0": 26, 
                "2100.0": 25, 
                "1700.0": 24, 
                "900.0": 28, 
                "1900.0": 28, 
                "700.0": 25
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 225, 
        "length": {
            "token": {
                "average": 5.74102, 
                "standard-deviation": 0.46951
            }, 
            "character": {
                "average": 5.74102, 
                "standard-deviation": 0.46951
            }
        }, 
        "numeric_density": 0.82582, 
        "numeric": {
            "Q1": 1000.0, 
            "Q3": 1835.5, 
            "standard-deviation": 508.20983, 
            "ratio": 1.0, 
            "Q2": 1420.0, 
            "mean": 1420.34168
        }, 
        "ratio_distinct_values": 0.24483, 
        "num_distinct_tokens": 225, 
        "decimal": {
            "Q1": 1000.0, 
            "Q3": 1835.5, 
            "standard-deviation": 508.20983, 
            "ratio": 1.0, 
            "Q2": 1420.0, 
            "mean": 1420.34168
        }
    }, 
    "county": {
        "ratio_distinct_tokens": 0.08842, 
        "num_integer": 0, 
        "language": {
            "fr": 21, 
            "en": 67, 
            "pt": 23, 
            "vi": 137, 
            "de": 395, 
            "sw": 168, 
            "cy": 2, 
            "tl": 75, 
            "id": 19, 
            "pl": 12
        }, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_values": {
                "ROSEAU": 14, 
                "STEARNS": 25, 
                "OLMSTED": 23, 
                "WASHINGTON": 46, 
                "ST LOUIS": 116, 
                "RAMSEY": 32, 
                "CLAY": 14, 
                "DAKOTA": 63, 
                "HENNEPIN": 105, 
                "ANOKA": 52
            }, 
            "most_common_tokens": {
                "ROSEAU": 14, 
                "STEARNS": 25, 
                "LOUIS": 116, 
                "OLMSTED": 23, 
                "WASHINGTON": 46, 
                "HENNEPIN": 105, 
                "RAMSEY": 32, 
                "DAKOTA": 63, 
                "ST": 116, 
                "ANOKA": 52
            }, 
            "most_common_alphanumeric_tokens": {
                "STEARNS": 25, 
                "LOUIS": 116, 
                "OLMSTED": 23, 
                "WASHINGTON": 46, 
                "HENNEPIN": 105, 
                "RAMSEY": 32, 
                "CLAY": 14, 
                "DAKOTA": 63, 
                "ST": 116, 
                "ANOKA": 52
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 85, 
        "length": {
            "token": {
                "average": 5.78943, 
                "standard-deviation": 2.09848
            }, 
            "character": {
                "average": 7.10446, 
                "standard-deviation": 1.81736
            }
        }, 
        "numeric_density": 0.0, 
        "ratio_distinct_values": 0.09249, 
        "num_distinct_tokens": 97
    }, 
    "county_code": {
        "ratio_distinct_tokens": 0.09249, 
        "num_integer": 919, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "24": 14, 
                "60": 32, 
                "25": 105, 
                "18": 63, 
                "53": 23, 
                "1": 52, 
                "65": 14, 
                "70": 25, 
                "69": 116, 
                "79": 46
            }, 
            "most_common_values": {
                "24": 14, 
                "60": 32, 
                "25": 105, 
                "18": 63, 
                "53": 23, 
                "1": 52, 
                "65": 14, 
                "70": 25, 
                "69": 116, 
                "79": 46
            }, 
            "most_common_tokens": {
                "24": 14, 
                "60": 32, 
                "25": 105, 
                "18": 63, 
                "53": 23, 
                "1": 52, 
                "65": 14, 
                "70": 25, 
                "69": 116, 
                "79": 46
            }, 
            "most_common_alphanumeric_tokens": {
                "24": 14, 
                "60": 32, 
                "25": 105, 
                "18": 63, 
                "53": 23, 
                "1": 52, 
                "65": 14, 
                "70": 25, 
                "69": 116, 
                "79": 46
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 85, 
        "length": {
            "token": {
                "average": 1.88357, 
                "standard-deviation": 0.32092
            }, 
            "character": {
                "average": 1.88357, 
                "standard-deviation": 0.32092
            }
        }, 
        "numeric_density": 1.0, 
        "numeric": {
            "Q1": 20.0, 
            "Q3": 69.0, 
            "standard-deviation": 25.67484, 
            "ratio": 1.0, 
            "Q2": 43.0, 
            "mean": 42.52339
        }, 
        "ratio_distinct_values": 0.09249, 
        "integer": {
            "Q1": 20.0, 
            "Q3": 69.0, 
            "standard-deviation": 25.67484, 
            "ratio": 1.0, 
            "Q2": 43.0, 
            "mean": 42.52339
        }, 
        "num_distinct_tokens": 85
    }, 
    "startdt": {
        "ratio_distinct_tokens": 0.0914, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "121387.0": 26, 
                "30388.0": 24, 
                "121687.0": 24, 
                "122787.0": 27, 
                "12688.0": 31, 
                "20288.0": 120, 
                "122687.0": 39, 
                "121287.0": 37, 
                "122887.0": 33, 
                "10188.0": 45
            }, 
            "most_common_values": {
                "121387.0": 26, 
                "30388.0": 24, 
                "121687.0": 24, 
                "122787.0": 27, 
                "12688.0": 31, 
                "20288.0": 120, 
                "122687.0": 39, 
                "121287.0": 37, 
                "122887.0": 33, 
                "10188.0": 45
            }, 
            "most_common_tokens": {
                "121387.0": 26, 
                "30388.0": 24, 
                "121687.0": 24, 
                "122787.0": 27, 
                "12688.0": 31, 
                "20288.0": 120, 
                "122687.0": 39, 
                "121287.0": 37, 
                "122887.0": 33, 
                "10188.0": 45
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 84, 
        "length": {
            "token": {
                "average": 7.39391, 
                "standard-deviation": 0.48888
            }, 
            "character": {
                "average": 7.39391, 
                "standard-deviation": 0.48888
            }
        }, 
        "numeric_density": 0.86475, 
        "numeric": {
            "Q1": 12688.0, 
            "Q3": 121687.0, 
            "standard-deviation": 51281.33374, 
            "ratio": 1.0, 
            "Q2": 22488.0, 
            "mean": 58827.32318
        }, 
        "ratio_distinct_values": 0.0914, 
        "num_distinct_tokens": 84, 
        "decimal": {
            "Q1": 12688.0, 
            "Q3": 121687.0, 
            "standard-deviation": 51281.33374, 
            "ratio": 1.0, 
            "Q2": 22488.0, 
            "mean": 58827.32318
        }
    }, 
    "radonFile_index": {
        "ratio_distinct_tokens": 1.0, 
        "num_integer": 919, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5458": 1, 
                "5289": 1, 
                "5618": 1, 
                "5983": 1, 
                "5962": 1, 
                "5963": 1, 
                "5964": 1, 
                "5965": 1, 
                "5849": 1, 
                "5848": 1
            }, 
            "most_common_values": {
                "5458": 1, 
                "5289": 1, 
                "5618": 1, 
                "5983": 1, 
                "5962": 1, 
                "5963": 1, 
                "5964": 1, 
                "5965": 1, 
                "5849": 1, 
                "5848": 1
            }, 
            "most_common_tokens": {
                "5458": 1, 
                "5289": 1, 
                "5618": 1, 
                "5983": 1, 
                "5962": 1, 
                "5963": 1, 
                "5964": 1, 
                "5965": 1, 
                "5849": 1, 
                "5848": 1
            }, 
            "most_common_alphanumeric_tokens": {
                "5458": 1, 
                "5289": 1, 
                "5618": 1, 
                "5983": 1, 
                "5962": 1, 
                "5963": 1, 
                "5964": 1, 
                "5965": 1, 
                "5849": 1, 
                "5848": 1
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 919, 
        "length": {
            "token": {
                "average": 4.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 4.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 1.0, 
        "numeric": {
            "Q1": 5310.5, 
            "Q3": 5769.5, 
            "standard-deviation": 265.43675, 
            "ratio": 1.0, 
            "Q2": 5540.0, 
            "mean": 5540.0
        }, 
        "ratio_distinct_values": 1.0, 
        "integer": {
            "Q1": 5310.5, 
            "Q3": 5769.5, 
            "standard-deviation": 265.43675, 
            "ratio": 1.0, 
            "Q2": 5540.0, 
            "mean": 5540.0
        }, 
        "num_distinct_tokens": 919
    }, 
    "zip": {
        "ratio_distinct_tokens": 0.4037, 
        "num_integer": 919, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "55082": 12, 
                "56001": 11, 
                "55075": 19, 
                "55303": 15, 
                "55807": 10, 
                "55804": 14, 
                "55025": 12, 
                "55304": 10, 
                "55033": 11, 
                "55746": 11
            }, 
            "most_common_values": {
                "55082": 12, 
                "56001": 11, 
                "55075": 19, 
                "55303": 15, 
                "55807": 10, 
                "55804": 14, 
                "55025": 12, 
                "55304": 10, 
                "55033": 11, 
                "55746": 11
            }, 
            "most_common_tokens": {
                "55082": 12, 
                "56001": 11, 
                "55075": 19, 
                "55303": 15, 
                "55807": 10, 
                "55804": 14, 
                "55025": 12, 
                "55304": 10, 
                "55033": 11, 
                "55746": 11
            }, 
            "most_common_alphanumeric_tokens": {
                "55082": 12, 
                "56001": 11, 
                "55075": 19, 
                "55303": 15, 
                "55807": 10, 
                "55804": 14, 
                "55025": 12, 
                "55304": 10, 
                "55033": 11, 
                "55746": 11
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 371, 
        "length": {
            "token": {
                "average": 5.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 5.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 1.0, 
        "numeric": {
            "Q1": 55318.0, 
            "Q3": 56119.5, 
            "standard-deviation": 516.7936, 
            "ratio": 1.0, 
            "Q2": 55746.0, 
            "mean": 55729.5778
        }, 
        "ratio_distinct_values": 0.4037, 
        "integer": {
            "Q1": 55318.0, 
            "Q3": 56119.5, 
            "standard-deviation": 516.7936, 
            "ratio": 1.0, 
            "Q2": 55746.0, 
            "mean": 55729.5778
        }, 
        "num_distinct_tokens": 371
    }, 
    "floor": {
        "ratio_distinct_tokens": 0.00218, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "0.0": 766, 
                "1.0": 153
            }, 
            "most_common_values": {
                "0.0": 766, 
                "1.0": 153
            }, 
            "most_common_tokens": {
                "0.0": 766, 
                "1.0": 153
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 2, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.37272, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.16649
        }, 
        "ratio_distinct_values": 0.00218, 
        "num_distinct_tokens": 2, 
        "decimal": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.37272, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.16649
        }
    }, 
    "rep": {
        "ratio_distinct_tokens": 0.00544, 
        "num_integer": 919, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "1": 194, 
                "3": 179, 
                "2": 196, 
                "5": 181, 
                "4": 169
            }, 
            "most_common_values": {
                "1": 194, 
                "3": 179, 
                "2": 196, 
                "5": 181, 
                "4": 169
            }, 
            "most_common_tokens": {
                "1": 194, 
                "3": 179, 
                "2": 196, 
                "5": 181, 
                "4": 169
            }, 
            "most_common_alphanumeric_tokens": {
                "1": 194, 
                "3": 179, 
                "2": 196, 
                "5": 181, 
                "4": 169
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 5, 
        "length": {
            "token": {
                "average": 1.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 1.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 1.0, 
        "numeric": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.42417, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 2.94233
        }, 
        "ratio_distinct_values": 0.00544, 
        "integer": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.42417, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 2.94233
        }, 
        "num_distinct_tokens": 5
    }, 
    "zipflag": {
        "ratio_distinct_tokens": 0.00218, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "0.0": 918, 
                "1.0": 1
            }, 
            "most_common_values": {
                "0.0": 918, 
                "1.0": 1
            }, 
            "most_common_tokens": {
                "0.0": 918, 
                "1.0": 1
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 2, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.03299, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.00109
        }, 
        "ratio_distinct_values": 0.00218, 
        "num_distinct_tokens": 2, 
        "decimal": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.03299, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.00109
        }
    }, 
    "dupflag": {
        "ratio_distinct_tokens": 0.00326, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "0.0": 857, 
                "2.0": 17, 
                "1.0": 45
            }, 
            "most_common_values": {
                "0.0": 857, 
                "2.0": 17, 
                "1.0": 45
            }, 
            "most_common_tokens": {
                "0.0": 857, 
                "2.0": 17, 
                "1.0": 45
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 3, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.34014, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.08596
        }, 
        "ratio_distinct_values": 0.00326, 
        "num_distinct_tokens": 3, 
        "decimal": {
            "Q1": 0.0, 
            "Q3": 0.0, 
            "standard-deviation": 0.34014, 
            "ratio": 1.0, 
            "Q2": 0.0, 
            "mean": 0.08596
        }
    }, 
    "state": {
        "ratio_distinct_tokens": 0.00109, 
        "num_integer": 0, 
        "language": {
            "sw": 919
        }, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_values": {
                "MN": 919
            }, 
            "most_common_tokens": {
                "MN": 919
            }, 
            "most_common_alphanumeric_tokens": {
                "MN": 919
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 1, 
        "length": {
            "token": {
                "average": 2.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 2.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.0, 
        "ratio_distinct_values": 0.00109, 
        "num_distinct_tokens": 1
    }, 
    "stratum": {
        "ratio_distinct_tokens": 0.00544, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5.0": 164, 
                "2.0": 274, 
                "1.0": 27, 
                "4.0": 158, 
                "3.0": 296
            }, 
            "most_common_values": {
                "5.0": 164, 
                "2.0": 274, 
                "1.0": 27, 
                "4.0": 158, 
                "3.0": 296
            }, 
            "most_common_tokens": {
                "5.0": 164, 
                "2.0": 274, 
                "1.0": 27, 
                "4.0": 158, 
                "3.0": 296
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 5, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.12838, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 3.17193
        }, 
        "ratio_distinct_values": 0.00544, 
        "num_distinct_tokens": 5, 
        "decimal": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.12838, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 3.17193
        }
    }, 
    "typebldg": {
        "ratio_distinct_tokens": 0.00544, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5.0": 8, 
                "0.0": 27, 
                "2.0": 27, 
                "1.0": 855, 
                "3.0": 2
            }, 
            "most_common_values": {
                "5.0": 8, 
                "0.0": 27, 
                "2.0": 27, 
                "1.0": 855, 
                "3.0": 2
            }, 
            "most_common_tokens": {
                "5.0": 8, 
                "0.0": 27, 
                "2.0": 27, 
                "1.0": 855, 
                "3.0": 2
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 5, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 1.0, 
            "Q3": 1.0, 
            "standard-deviation": 0.45325, 
            "ratio": 1.0, 
            "Q2": 1.0, 
            "mean": 1.03917
        }, 
        "ratio_distinct_values": 0.00544, 
        "num_distinct_tokens": 5, 
        "decimal": {
            "Q1": 1.0, 
            "Q3": 1.0, 
            "standard-deviation": 0.45325, 
            "ratio": 1.0, 
            "Q2": 1.0, 
            "mean": 1.03917
        }
    }, 
    "Uppm": {
        "ratio_distinct_tokens": 0.09249, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "1.31208": 14, 
                "0.907991": 105, 
                "0.658327": 32, 
                "1.12344": 25, 
                "0.808928": 14, 
                "0.428565": 52, 
                "0.622088": 116, 
                "0.862876": 46, 
                "0.976144": 63, 
                "1.27526": 23
            }, 
            "most_common_values": {
                "1.31208": 14, 
                "0.907991": 105, 
                "0.658327": 32, 
                "1.12344": 25, 
                "0.808928": 14, 
                "0.428565": 52, 
                "0.622088": 116, 
                "0.862876": 46, 
                "0.976144": 63, 
                "1.27526": 23
            }, 
            "most_common_tokens": {
                "1.31208": 14, 
                "0.907991": 105, 
                "0.658327": 32, 
                "1.12344": 25, 
                "0.808928": 14, 
                "0.428565": 52, 
                "0.622088": 116, 
                "0.862876": 46, 
                "0.976144": 63, 
                "1.27526": 23
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 85, 
        "length": {
            "token": {
                "average": 8.47008, 
                "standard-deviation": 2.88277
            }, 
            "character": {
                "average": 8.47008, 
                "standard-deviation": 2.88277
            }
        }, 
        "numeric_density": 0.88194, 
        "numeric": {
            "Q1": 0.62209, 
            "Q3": 1.2011, 
            "standard-deviation": 0.32009, 
            "ratio": 1.0, 
            "Q2": 0.90799, 
            "mean": 0.93391
        }, 
        "ratio_distinct_values": 0.09249, 
        "num_distinct_tokens": 85, 
        "decimal": {
            "Q1": 0.62209, 
            "Q3": 1.2011, 
            "standard-deviation": 0.32009, 
            "ratio": 1.0, 
            "Q2": 0.90799, 
            "mean": 0.93391
        }
    }, 
    "stfips": {
        "ratio_distinct_tokens": 0.00109, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "27.0": 919
            }, 
            "most_common_values": {
                "27.0": 919
            }, 
            "most_common_tokens": {
                "27.0": 919
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 1, 
        "length": {
            "token": {
                "average": 4.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 4.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.75, 
        "numeric": {
            "Q1": 27.0, 
            "Q3": 27.0, 
            "standard-deviation": 0.0, 
            "ratio": 1.0, 
            "Q2": 27.0, 
            "mean": 27.0
        }, 
        "ratio_distinct_values": 0.00109, 
        "num_distinct_tokens": 1, 
        "decimal": {
            "Q1": 27.0, 
            "Q3": 27.0, 
            "standard-deviation": 0.0, 
            "ratio": 1.0, 
            "Q2": 27.0, 
            "mean": 27.0
        }
    }, 
    "stopdt": {
        "ratio_distinct_tokens": 0.0914, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "123087.0": 31, 
                "12888.0": 30, 
                "121487.0": 35, 
                "30388.0": 28, 
                "20288.0": 118, 
                "10188.0": 52, 
                "122887.0": 38, 
                "122987.0": 27, 
                "121587.0": 24, 
                "11988.0": 26
            }, 
            "most_common_values": {
                "123087.0": 31, 
                "12888.0": 30, 
                "121487.0": 35, 
                "30388.0": 28, 
                "20288.0": 118, 
                "10188.0": 52, 
                "122887.0": 38, 
                "122987.0": 27, 
                "121587.0": 24, 
                "11988.0": 26
            }, 
            "most_common_tokens": {
                "123087.0": 31, 
                "12888.0": 30, 
                "121487.0": 35, 
                "30388.0": 28, 
                "20288.0": 118, 
                "10188.0": 52, 
                "122887.0": 38, 
                "122987.0": 27, 
                "121587.0": 24, 
                "11988.0": 26
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 84, 
        "length": {
            "token": {
                "average": 7.37541, 
                "standard-deviation": 0.48449
            }, 
            "character": {
                "average": 7.37541, 
                "standard-deviation": 0.48449
            }
        }, 
        "numeric_density": 0.86441, 
        "numeric": {
            "Q1": 12638.0, 
            "Q3": 121787.0, 
            "standard-deviation": 50830.21873, 
            "ratio": 1.0, 
            "Q2": 22588.0, 
            "mean": 57139.74646
        }, 
        "ratio_distinct_values": 0.0914, 
        "num_distinct_tokens": 84, 
        "decimal": {
            "Q1": 12638.0, 
            "Q3": 121787.0, 
            "standard-deviation": 50830.21873, 
            "ratio": 1.0, 
            "Q2": 22588.0, 
            "mean": 57139.74646
        }
    }, 
    "pcterr": {
        "ratio_distinct_tokens": 0.2568, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5.1": 16, 
                "4.2": 12, 
                "0.0": 17, 
                "7.0": 14, 
                "10.8": 12, 
                "4.4": 12, 
                "7.8": 12, 
                "9.0": 11, 
                "3.8": 11, 
                "3.9": 13
            }, 
            "most_common_values": {
                "5.1": 16, 
                "4.2": 12, 
                "0.0": 17, 
                "7.0": 14, 
                "10.8": 12, 
                "4.4": 12, 
                "7.8": 12, 
                "9.0": 11, 
                "3.8": 11, 
                "3.9": 13
            }, 
            "most_common_tokens": {
                "5.1": 16, 
                "4.2": 12, 
                "0.0": 17, 
                "7.0": 14, 
                "10.8": 12, 
                "4.4": 12, 
                "7.8": 12, 
                "9.0": 11, 
                "3.8": 11, 
                "3.9": 13
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 236, 
        "length": {
            "token": {
                "average": 3.36997, 
                "standard-deviation": 0.48306
            }, 
            "character": {
                "average": 3.36997, 
                "standard-deviation": 0.48306
            }
        }, 
        "numeric_density": 0.70326, 
        "numeric": {
            "Q1": 5.2, 
            "Q3": 12.7, 
            "standard-deviation": 8.47754, 
            "ratio": 1.0, 
            "Q2": 8.1, 
            "mean": 10.48172
        }, 
        "ratio_distinct_values": 0.2568, 
        "num_distinct_tokens": 236, 
        "decimal": {
            "Q1": 5.2, 
            "Q3": 12.7, 
            "standard-deviation": 8.47754, 
            "ratio": 1.0, 
            "Q2": 8.1, 
            "mean": 10.48172
        }
    }, 
    "wave": {
        "ratio_distinct_tokens": 0.037, 
        "num_integer": 919, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "24": 28, 
                "26": 33, 
                "22": 35, 
                "47": 30, 
                "44": 31, 
                "30": 30, 
                "28": 31, 
                "36": 31, 
                "40": 29, 
                "34": 35
            }, 
            "most_common_values": {
                "24": 28, 
                "26": 33, 
                "22": 35, 
                "47": 30, 
                "44": 31, 
                "30": 30, 
                "28": 31, 
                "36": 31, 
                "40": 29, 
                "34": 35
            }, 
            "most_common_tokens": {
                "24": 28, 
                "26": 33, 
                "22": 35, 
                "47": 30, 
                "44": 31, 
                "30": 30, 
                "28": 31, 
                "36": 31, 
                "40": 29, 
                "34": 35
            }, 
            "most_common_alphanumeric_tokens": {
                "24": 28, 
                "26": 33, 
                "22": 35, 
                "47": 30, 
                "44": 31, 
                "30": 30, 
                "28": 31, 
                "36": 31, 
                "40": 29, 
                "34": 35
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 34, 
        "length": {
            "token": {
                "average": 1.89663, 
                "standard-deviation": 0.30461
            }, 
            "character": {
                "average": 1.89663, 
                "standard-deviation": 0.30461
            }
        }, 
        "numeric_density": 1.0, 
        "numeric": {
            "Q1": 25.0, 
            "Q3": 42.0, 
            "standard-deviation": 13.00527, 
            "ratio": 1.0, 
            "Q2": 34.0, 
            "mean": 32.01306
        }, 
        "ratio_distinct_values": 0.037, 
        "integer": {
            "Q1": 25.0, 
            "Q3": 42.0, 
            "standard-deviation": 13.00527, 
            "ratio": 1.0, 
            "Q2": 34.0, 
            "mean": 32.01306
        }, 
        "num_distinct_tokens": 34
    }, 
    "state2": {
        "ratio_distinct_tokens": 0.00109, 
        "num_integer": 0, 
        "language": {
            "sw": 919
        }, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_values": {
                "MN": 919
            }, 
            "most_common_tokens": {
                "MN": 919
            }, 
            "most_common_alphanumeric_tokens": {
                "MN": 919
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 1, 
        "length": {
            "token": {
                "average": 2.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 2.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.0, 
        "ratio_distinct_values": 0.00109, 
        "num_distinct_tokens": 1
    }, 
    "starttm": {
        "ratio_distinct_tokens": 0.20566, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "1830.0": 24, 
                "1800.0": 32, 
                "800.0": 38, 
                "1000.0": 37, 
                "1600.0": 28, 
                "2100.0": 27, 
                "1700.0": 26, 
                "900.0": 35, 
                "1900.0": 29, 
                "1100.0": 29
            }, 
            "most_common_values": {
                "1830.0": 24, 
                "1800.0": 32, 
                "800.0": 38, 
                "1000.0": 37, 
                "1600.0": 28, 
                "2100.0": 27, 
                "1700.0": 26, 
                "900.0": 35, 
                "1900.0": 29, 
                "1100.0": 29
            }, 
            "most_common_tokens": {
                "1830.0": 24, 
                "1800.0": 32, 
                "800.0": 38, 
                "1000.0": 37, 
                "1600.0": 28, 
                "2100.0": 27, 
                "1700.0": 26, 
                "900.0": 35, 
                "1900.0": 29, 
                "1100.0": 29
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 189, 
        "length": {
            "token": {
                "average": 5.75299, 
                "standard-deviation": 0.4464
            }, 
            "character": {
                "average": 5.75299, 
                "standard-deviation": 0.4464
            }
        }, 
        "numeric_density": 0.82618, 
        "numeric": {
            "Q1": 1000.0, 
            "Q3": 1817.5, 
            "standard-deviation": 483.2707, 
            "ratio": 1.0, 
            "Q2": 1415.0, 
            "mean": 1413.82481
        }, 
        "ratio_distinct_values": 0.20566, 
        "num_distinct_tokens": 189, 
        "decimal": {
            "Q1": 1000.0, 
            "Q3": 1817.5, 
            "standard-deviation": 483.2707, 
            "ratio": 1.0, 
            "Q2": 1415.0, 
            "mean": 1413.82481
        }
    }, 
    "fips": {
        "ratio_distinct_tokens": 0.09249, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "27137.0": 116, 
                "27037.0": 63, 
                "27145.0": 25, 
                "27123.0": 32, 
                "27163.0": 46, 
                "27027.0": 14, 
                "27003.0": 52, 
                "27053.0": 105, 
                "27135.0": 14, 
                "27109.0": 23
            }, 
            "most_common_values": {
                "27137.0": 116, 
                "27037.0": 63, 
                "27145.0": 25, 
                "27123.0": 32, 
                "27163.0": 46, 
                "27027.0": 14, 
                "27003.0": 52, 
                "27053.0": 105, 
                "27135.0": 14, 
                "27109.0": 23
            }, 
            "most_common_tokens": {
                "27137.0": 116, 
                "27037.0": 63, 
                "27145.0": 25, 
                "27123.0": 32, 
                "27163.0": 46, 
                "27027.0": 14, 
                "27003.0": 52, 
                "27053.0": 105, 
                "27135.0": 14, 
                "27109.0": 23
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 85, 
        "length": {
            "token": {
                "average": 7.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 7.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.85714, 
        "numeric": {
            "Q1": 27041.0, 
            "Q3": 27137.0, 
            "standard-deviation": 52.12624, 
            "ratio": 1.0, 
            "Q2": 27085.0, 
            "mean": 27087.41349
        }, 
        "ratio_distinct_values": 0.09249, 
        "num_distinct_tokens": 85, 
        "decimal": {
            "Q1": 27041.0, 
            "Q3": 27137.0, 
            "standard-deviation": 52.12624, 
            "ratio": 1.0, 
            "Q2": 27085.0, 
            "mean": 27087.41349
        }
    }, 
    "basement": {
        "ratio_distinct_tokens": 0.00313, 
        "num_integer": 0, 
        "language": {
            "vi": 59, 
            "cy": 819
        }, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_values": {
                "Y": 819, 
                " ": 41, 
                "N": 59
            }, 
            "most_common_tokens": {
                "Y": 819, 
                "N": 59
            }, 
            "most_common_alphanumeric_tokens": {
                "Y": 819, 
                "N": 59
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 3, 
        "length": {
            "token": {
                "average": 0.91458, 
                "standard-deviation": 0.27965
            }, 
            "character": {
                "average": 1.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.0, 
        "ratio_distinct_values": 0.00326, 
        "num_distinct_tokens": 3
    }, 
    "room": {
        "ratio_distinct_tokens": 0.00762, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5.0": 12, 
                "1.0": 47, 
                "4.0": 425, 
                "0.0": 57, 
                "7.0": 70, 
                "3.0": 106, 
                "2.0": 202
            }, 
            "most_common_values": {
                "5.0": 12, 
                "1.0": 47, 
                "4.0": 425, 
                "0.0": 57, 
                "7.0": 70, 
                "3.0": 106, 
                "2.0": 202
            }, 
            "most_common_tokens": {
                "5.0": 12, 
                "1.0": 47, 
                "4.0": 425, 
                "0.0": 57, 
                "7.0": 70, 
                "3.0": 106, 
                "2.0": 202
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 7, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.62407, 
            "ratio": 1.0, 
            "Q2": 4.0, 
            "mean": 3.28509
        }, 
        "ratio_distinct_values": 0.00762, 
        "num_distinct_tokens": 7, 
        "decimal": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.62407, 
            "ratio": 1.0, 
            "Q2": 4.0, 
            "mean": 3.28509
        }
    }, 
    "region": {
        "ratio_distinct_tokens": 0.00544, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "5.0": 190, 
                "2.0": 160, 
                "1.0": 127, 
                "4.0": 144, 
                "3.0": 298
            }, 
            "most_common_values": {
                "5.0": 190, 
                "2.0": 160, 
                "1.0": 127, 
                "4.0": 144, 
                "3.0": 298
            }, 
            "most_common_tokens": {
                "5.0": 190, 
                "2.0": 160, 
                "1.0": 127, 
                "4.0": 144, 
                "3.0": 298
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 5, 
        "length": {
            "token": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 3.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.66667, 
        "numeric": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.3031, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 3.1197
        }, 
        "ratio_distinct_values": 0.00544, 
        "num_distinct_tokens": 5, 
        "decimal": {
            "Q1": 2.0, 
            "Q3": 4.0, 
            "standard-deviation": 1.3031, 
            "ratio": 1.0, 
            "Q2": 3.0, 
            "mean": 3.1197
        }
    }, 
    "adjwt": {
        "ratio_distinct_tokens": 0.02503, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "471.3662230000001": 56, 
                "485.435931": 52, 
                "1024.442902": 64, 
                "921.864905": 67, 
                "893.2374300000001": 61, 
                "461.274696": 50, 
                "433.316718": 60, 
                "1071.318034": 51, 
                "461.62367": 56, 
                "990.411554": 53
            }, 
            "most_common_values": {
                "471.3662230000001": 56, 
                "485.435931": 52, 
                "1024.442902": 64, 
                "921.864905": 67, 
                "893.2374300000001": 61, 
                "461.274696": 50, 
                "433.316718": 60, 
                "1071.318034": 51, 
                "461.62367": 56, 
                "990.411554": 53
            }, 
            "most_common_tokens": {
                "471.3662230000001": 56, 
                "485.435931": 52, 
                "1024.442902": 64, 
                "921.864905": 67, 
                "893.2374300000001": 61, 
                "461.274696": 50, 
                "433.316718": 60, 
                "1071.318034": 51, 
                "461.62367": 56, 
                "990.411554": 53
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 23, 
        "length": {
            "token": {
                "average": 11.23395, 
                "standard-deviation": 2.27727
            }, 
            "character": {
                "average": 11.23395, 
                "standard-deviation": 2.27727
            }
        }, 
        "numeric_density": 0.91098, 
        "numeric": {
            "Q1": 471.36622, 
            "Q3": 1146.49919, 
            "standard-deviation": 595.84153, 
            "ratio": 1.0, 
            "Q2": 990.41155, 
            "mean": 1051.68193
        }, 
        "ratio_distinct_values": 0.02503, 
        "num_distinct_tokens": 23, 
        "decimal": {
            "Q1": 471.36622, 
            "Q3": 1146.49919, 
            "standard-deviation": 595.84153, 
            "ratio": 1.0, 
            "Q2": 990.41155, 
            "mean": 1051.68193
        }
    }, 
    "windoor": {
        "ratio_distinct_tokens": 0.00054, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 0, 
        "frequent-entries": {
            "most_common_values": {
                " ": 919
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 1, 
        "length": {
            "token": {
                "average": 0.0, 
                "standard-deviation": 0.0
            }, 
            "character": {
                "average": 1.0, 
                "standard-deviation": 0.0
            }
        }, 
        "numeric_density": 0.0, 
        "ratio_distinct_values": 0.00109, 
        "num_distinct_tokens": 1
    }, 
    "cntyfips": {
        "ratio_distinct_tokens": 0.09249, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "53.0": 105, 
                "123.0": 32, 
                "137.0": 116, 
                "3.0": 52, 
                "49.0": 14, 
                "37.0": 63, 
                "163.0": 46, 
                "109.0": 23, 
                "13.0": 14, 
                "145.0": 25
            }, 
            "most_common_values": {
                "53.0": 105, 
                "123.0": 32, 
                "137.0": 116, 
                "3.0": 52, 
                "49.0": 14, 
                "37.0": 63, 
                "163.0": 46, 
                "109.0": 23, 
                "13.0": 14, 
                "145.0": 25
            }, 
            "most_common_tokens": {
                "53.0": 105, 
                "123.0": 32, 
                "137.0": 116, 
                "3.0": 52, 
                "49.0": 14, 
                "37.0": 63, 
                "163.0": 46, 
                "109.0": 23, 
                "13.0": 14, 
                "145.0": 25
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 85, 
        "length": {
            "token": {
                "average": 4.37106, 
                "standard-deviation": 0.6214
            }, 
            "character": {
                "average": 4.37106, 
                "standard-deviation": 0.6214
            }
        }, 
        "numeric_density": 0.77122, 
        "numeric": {
            "Q1": 41.0, 
            "Q3": 137.0, 
            "standard-deviation": 52.12624, 
            "ratio": 1.0, 
            "Q2": 85.0, 
            "mean": 87.41349
        }, 
        "ratio_distinct_values": 0.09249, 
        "num_distinct_tokens": 85, 
        "decimal": {
            "Q1": 41.0, 
            "Q3": 137.0, 
            "standard-deviation": 52.12624, 
            "ratio": 1.0, 
            "Q2": 85.0, 
            "mean": 87.41349
        }
    }, 
    "activity": {
        "ratio_distinct_tokens": 0.16975, 
        "num_integer": 0, 
        "language": {}, 
        "num_decimal": 919, 
        "frequent-entries": {
            "most_common_numeric_tokens": {
                "1.4": 18, 
                "1.5": 24, 
                "1.6": 18, 
                "1.7": 18, 
                "1.1": 18, 
                "1.8": 25, 
                "2.9": 20, 
                "2.8": 18, 
                "2.2": 19, 
                "2.1": 19
            }, 
            "most_common_values": {
                "1.4": 18, 
                "1.5": 24, 
                "1.6": 18, 
                "1.7": 18, 
                "1.1": 18, 
                "1.8": 25, 
                "2.9": 20, 
                "2.8": 18, 
                "2.2": 19, 
                "2.1": 19
            }, 
            "most_common_tokens": {
                "1.4": 18, 
                "1.5": 24, 
                "1.6": 18, 
                "1.7": 18, 
                "1.1": 18, 
                "1.8": 25, 
                "2.9": 20, 
                "2.8": 18, 
                "2.2": 19, 
                "2.1": 19
            }
        }, 
        "num_nonblank": 919, 
        "num_missing": 0, 
        "num_distinct_values": 156, 
        "length": {
            "token": {
                "average": 3.09249, 
                "standard-deviation": 0.28988
            }, 
            "character": {
                "average": 3.09249, 
                "standard-deviation": 0.28988
            }
        }, 
        "numeric_density": 0.67664, 
        "numeric": {
            "Q1": 1.9, 
            "Q3": 6.0, 
            "standard-deviation": 4.48158, 
            "ratio": 1.0, 
            "Q2": 3.6, 
            "mean": 4.76812
        }, 
        "ratio_distinct_values": 0.16975, 
        "num_distinct_tokens": 156, 
        "decimal": {
            "Q1": 1.9, 
            "Q3": 6.0, 
            "standard-deviation": 4.48158, 
            "ratio": 1.0, 
            "Q2": 3.6, 
            "mean": 4.76812
        }
    }
}
```
