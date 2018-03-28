from dsbox.datapreprocessing.profiler import Profiler, Hyperparams
from d3m.container import dataset
from d3m.metadata import hyperparams

hp = Hyperparams({'features': ['target_values', 'ratio_of_tokens_split_by_punctuation_containing_numeric_char']})

# 1. dataset.Dataset as input
# dataset_doc_path = "/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/metadata/tests/data/datasets/iris_dataset_1/datasetDoc.json"
dataset_doc_path = "/nas/home/fangaol/seed_datasets_current/38_sick/TRAIN/dataset_TRAIN/datasetDoc.json"
ds = dataset.Dataset.load('file://{dataset_doc_path}'.format(dataset_doc_path=dataset_doc_path))

profiler = Profiler(hyperparams=Hyperparams())
result = profiler.produce(inputs=ds)

result.metadata.query(("0", "1", 1,) )
result.metadata.query(("0", metadata.base.ALL_ELEMENTS, 1,) )

# 2. DataFrame as input
import pandas as pd
# data = pd.read_csv("/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/metadata/tests/data/datasets/iris_dataset_1/tables/learningData.csv")
data = pd.read_csv("/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/dsbox-profiling/dsbox/datapreprocessing/profiler/unit_tests/sources/testData.csv")
profiler2 = Profiler(hyperparams=Hyperparams())
result2 = profiler2.produce(inputs=data)

result2.metadata.query(("0", "1", 1,) )
result2.metadata.query(("0", metadata.ALL_ELEMENTS, 1,) )
