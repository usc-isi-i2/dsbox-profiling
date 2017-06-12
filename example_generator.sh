start_time=`date +%s`

python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_26/data/raw_data/radon.csv dsbox/datapreprocessing/profiler/examples/profiled_r26_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_30/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_r30_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_32/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_r32_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_38/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_o38_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_313/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_o_313_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_185/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_o_185_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_196/data/trainData.csv dsbox/datapreprocessing/profiler/examples/profiled_o_196_trainData.json

end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.