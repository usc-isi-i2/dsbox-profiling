from dsbox.datapreprocessing.profiler import Profiler
from d3m_metadata.container import dataset 
from d3m_metadata import hyperparams, metadata

class Hyperparams(hyperparams.Hyperparams):
    pass

# 1. dataset as input
dataset_doc_path = "/Users/luofanghao/work/USC_lab/isi-II/work/DSBox_project/end2end_sys/metadata/tests/data/datasets/iris_dataset_1/datasetDoc.json"
ds = dataset.Dataset.load('file://{dataset_doc_path}'.format(dataset_doc_path=dataset_doc_path))

profiler = Profiler(hyperparams=Hyperparams())
result = profiler.produce(inputs=ds)

result.metadata.query(("0", "1", 1,) )
result.metadata.query(("0", metadata.ALL_ELEMENTS, 1,) )