from dsbox.datapreprocessing.profiler import Profiler, Hyperparams
from d3m.container import dataset
from d3m.metadata import hyperparams
from d3m import metadata
hp = Hyperparams({'features': ['target_values', 'ratio_of_tokens_split_by_punctuation_containing_numeric_char']})

# 1. dataset.Dataset as input
# dataset_doc_path = "/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/metadata/tests/data/datasets/iris_dataset_1/datasetDoc.json"
dataset_doc_path = "/nas/home/fangaol/seed_datasets_current/38_sick/TRAIN/dataset_TRAIN/datasetDoc.json"
ds = dataset.Dataset.load('file://{dataset_doc_path}'.format(dataset_doc_path=dataset_doc_path))

profiler = Profiler(hyperparams=hp)
result = profiler.produce(inputs=ds)

print(result.metadata.query(("0", "1", 1,) ))
a = result.metadata.query(("0", metadata.base.ALL_ELEMENTS, 1,) )

for i in a:
    print(i)
