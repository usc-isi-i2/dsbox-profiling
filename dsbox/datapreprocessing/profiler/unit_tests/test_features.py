import json
import numbers
import os
import pandas as pd
import unittest

from numpy.testing.utils import assert_approx_equal

from d3m import container
from d3m.metadata.base import ALL_ELEMENTS
from dsbox.datapreprocessing.profiler import Profiler, Hyperparams

class TestFeatures(unittest.TestCase):
    def setUp(self):
        gt_file = os.path.join(os.path.dirname(__file__), 'sources', 'gt.json')
        with open(gt_file) as data_file:
            self.ground_truth = json.load(data_file)

        self.param = Hyperparams({'metafeatures': set([
            'ratio_of_values_containing_numeric_char', 'ratio_of_numeric_values',
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
            'pearson_correlation_of_features', 'semantic_types'])})

        profiler = Profiler(hyperparams=self.param)

        test_data_file = os.path.join(os.path.dirname(__file__), 'sources', 'testData.csv')
        # df = container.DataFrame(pd.read_csv(test_data_file, dtype='str'))
        self.df = container.DataFrame(pd.read_csv(test_data_file))

        self.profiler_result = profiler.produce(inputs=self.df).value.metadata


    def compare(self, gt, pr, context):
        if isinstance(gt, dict):
            self.assertTrue(isinstance(gt, dict), context)
            for key, value in gt.items():
                self.assertTrue(key in pr, context + 'dict[{}] '.format(key))
                self.compare(value, gt[key], context + 'dict[{}] '.format(key))
        elif isinstance(gt, list):
            self.assertTrue(isinstance(pr, list) or isinstance(pr, tuple) , context)
            self.assertEqual(len(gt), len(pr), context + 'list ')
            for i in range(len(gt)):
                self.compare(gt[i], pr[i], context + 'list[{}] '.format(i))
        elif isinstance(gt, numbers.Number):
            assert_approx_equal(gt, pr)
        else:
            self.assertEqual(gt, pr)

    def test_all(self):
        """
        test main function. Only check the if the existed items in ground_truth also exist in profiler result.
        For the items that only exists in profiler result, will be ignored and pass the test.
        """
        for index, column_name in enumerate(self.df.columns):
            for feature in self.param['metafeatures']:
                if feature in self.ground_truth[index]:
                    gt = self.ground_truth[index][feature]
                    pr = self.profiler_result.query((ALL_ELEMENTS, index))[feature]
                    self.compare(gt, pr, 'column={} feature={} '.format(column_name, feature))

if __name__ == '__main__':
    unittest.main()
