from dsbox.datapreprocessing.profiler import Profiler, Hyperparams
from d3m.container import dataset
from d3m.metadata import hyperparams
from d3m import metadata

# first, specify the metafeaures that you want to compute
feature_names = ['ratio_of_values_containing_numeric_char', 'ratio_of_numeric_values',
    'number_of_outlier_numeric_values', 'num_filename']
hp = Hyperparams({'metafeatures' : set(feature_names)})

# 1. dataset.Dataset as input
# dataset_doc_path = "/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/seed_datasets_current/38_sick/TRAIN/dataset_TRAIN/datasetDoc.json"
dataset_doc_path = '/nfs1/dsbox-repo/data/datasets/seed_datasets_current/185_baseball/185_baseball_dataset/datasetDoc.json'
ds = dataset.Dataset.load('file://{dataset_doc_path}'.format(dataset_doc_path=dataset_doc_path))

profiler = Profiler(hyperparams=hp)
result = profiler.produce(inputs=ds).value

print(result.metadata.query(("0", "1", 1,) ))
a = result.metadata.query(("0", metadata.base.ALL_ELEMENTS, 1,) )

for i in a:
    print(i)

result.metadata.pretty_print()

# 2. DataFrame as input
import pandas as pd
# data = pd.read_csv("/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/dsbox-profiling/dsbox/datapreprocessing/profiler/unit_tests/sources/testData.csv")
data = pd.read_csv('/nfs1/dsbox-repo/data/datasets/seed_datasets_current/185_baseball/185_baseball_dataset/tables/learningData.csv')
profiler2 = Profiler(hyperparams=hp)
result2 = profiler2.produce(inputs=data).value

result2.metadata.query(("0", "1", 1,) )
result2.metadata.query(("0", metadata.base.ALL_ELEMENTS, 1,) )
result2.metadata.pretty_print()
