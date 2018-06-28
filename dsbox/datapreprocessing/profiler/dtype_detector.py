import typing
from typing import Any, Callable, List, Dict, Union, Optional, Sequence, Tuple

import d3m.metadata.base as mbase
import pandas as pd
from common_primitives import utils
from d3m import container
from d3m.container import DataFrame as d3m_DataFrame
from d3m.metadata import hyperparams, params
from d3m.primitive_interfaces.base import CallResult
from d3m.primitive_interfaces.base import CallResult
from d3m.primitive_interfaces.transformer import TransformerPrimitiveBase

from . import config


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def detector(inputs):

    lookup = {"float": ('http://schema.org/Float', 'https://metadata.datadrivendiscovery.org/types/Attribute'),
              "int": ('http://schema.org/Integer', 'https://metadata.datadrivendiscovery.org/types/Attribute'),
              "Categorical": ('https://metadata.datadrivendiscovery.org/types/CategoricalData',
                              'https://metadata.datadrivendiscovery.org/types/Attribute'),
              "Ordinal": ('https://metadata.datadrivendiscovery.org/types/OrdinalData',
                          'https://metadata.datadrivendiscovery.org/types/Attribute')
              }

    print("integer and float detector \n")


    for col in range(inputs.shape[1]):
        temp = inputs.iloc[:, col]
        old_metadata = dict(inputs.metadata.query((mbase.ALL_ELEMENTS, col)))
        dtype = pd.DataFrame(temp.dropna().str.isnumeric().value_counts())
        ## if there is already a data type, see if that is equal to what we identified, else update
        ## corner case : Integer type, could be a categorical Arrtribute
        # detetct integers and update metadata
        
        if True in dtype.index:
            if dtype.loc[True][0] == temp.dropna().shape[0]:
                if old_metadata["semantic_types"] == lookup["int"] or old_metadata["semantic_types"] == lookup[
                    "Categorical"] or old_metadata["semantic_types"] == lookup["Ordinal"]:
                    old_metadata["structural_type"] = type(10)

                else:
                    temp_value = list(old_metadata["semantic_types"])
                    if len(temp_value) >= 1:
                        old_metadata["semantic_types"] = ('http://schema.org/Integer', temp_value[-1])
                    else:
                        old_metadata["semantic_types"] = ('http://schema.org/Integer')
                    old_metadata["structural_type"] = type(10)
        # detetct Float and update metadata
        else:
            dtype = pd.DataFrame(temp.dropna().apply(isfloat).value_counts())
            if True in dtype.index:
                if dtype.loc[True][0] == temp.dropna().shape[0]:
                    if old_metadata["semantic_types"] == lookup["float"] or old_metadata["semantic_types"] == lookup[
                    "Categorical"] or old_metadata["semantic_types"] == lookup["Ordinal"]:
                        old_metadata["structural_type"] = type(10.0)
                    else:
                        temp_value = list(old_metadata["semantic_types"])
                        if len(temp_value) > 1:
                            old_metadata["semantic_types"] = ('http://schema.org/Float', temp_value[-1])
                        else:
                            old_metadata["semantic_types"] = ('http://schema.org/Float')
                        old_metadata["structural_type"] = type(10.0)
        inputs.metadata = inputs.metadata.update((mbase.ALL_ELEMENTS, col), old_metadata)

    return inputs


