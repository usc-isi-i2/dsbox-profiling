start_time=`date +%s`

python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_26/original/data/raw_data/radon.csv examples/profiled_r26_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_30/original/data/trainData.csv examples/profiled_r30_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/r_32/original/data/trainData.csv examples/profiled_r32_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_38/original/data/trainData.csv examples/profiled_o38_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_313/original/data/trainData.csv examples/profiled_o313_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_185/original/data/trainData.csv examples/profiled_o185_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_196/original/data/trainData.csv examples/profiled_o196_trainData.json
python dsbox/datapreprocessing/profiler/data_profile.py ../dsbox-data/o_4550/original/data/trainData.csv examples/profiled_o4550_trainData.json

end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.



# cp examples/profiled_r26_trainData.json   ../dsbox-data/r_26/profiled/
# cp examples/profiled_r30_trainData.json  ../dsbox-data/r_30/profiled/
# cp examples/profiled_r32_trainData.json  ../dsbox-data/r_32/profiled/
# cp examples/profiled_o38_trainData.json  ../dsbox-data/o_38/profiled/
# cp examples/profiled_o313_trainData.json  ../dsbox-data/o_313/profiled/
# cp examples/profiled_o185_trainData.json  ../dsbox-data/o_185/profiled/
# cp examples/profiled_o196_trainData.json  ../dsbox-data/o_196/profiled/
# cp examples/profiled_o4550_trainData.json  ../dsbox-data/o_4550/profiled/