import os
import re
import shutil

new_sr = 22050

corpus = '/media/share/datasets/aligner_benchmarks/sorted_quebec_french'
sorted_corpus = '/media/share/datasets/aligner_benchmarks/sorted_quebec_french'


old_directory = '/media/share/datasets/aligner_benchmarks/AlignerTestData/2_French_2000files'
new_directory = '/media/share/datasets/aligner_benchmarks/sorted_quebec_french'

for f in os.listdir(old_directory):
    if not any(f.lower().endswith(x) for x in ['.wav', '.lab']):
        continue
    name, ext = os.path.splitext(f)
    splitname = name.split('_')
    speaker_id = '_'.join(splitname[:2])
    speaker_dir = os.path.join(new_directory, speaker_id)
    os.makedirs(speaker_dir, exist_ok = True)

    old_path = os.path.join(old_directory, f)
    new_path = os.path.join(speaker_dir, f)
    shutil.copyfile(old_path, new_path)
