import sys
import shutil, os
sys.path.insert(0, os.path.expanduser('~/Montreal-Forced-Aligner'))

import time
import logging
import platform
import csv
import statistics
from datetime import datetime

from aligner.command_line.train_and_align import align_corpus

#corpus_dir = '/media/share/datasets/aligner_benchmarks/LibriSpeech/standard'
corpus_dir = '/media/share/datasets/aligner_benchmarks/sorted_tagalog'
#dict_path = os.path.expanduser('~/Montreal-Forced-Aligner/librispeech-lexicon.txt')
dict_path = None
#output_directory = '/data/michaela/aligned_librispeech'
output_directory = '/data/michaela/aligned_tagalog'
output_model_path = os.path.expanduser('~/Documents/tagalog_models.zip')
num_jobs = 2

def benchmark_align_corpus(corpus_dir, dict_path, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose):
    beg = time.time()
    align_corpus(corpus_dir, dict_path, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose)
    end = time.time()
    return [(end - beg)]

def benchmark_align_corpus_no_dict(corpus_dir, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose):
    beg = time.time()
    align_corpus(corpus_dir, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose)
    end = time.time()
    return [(end - beg)]

if dict_path == None:
    benchmark_align_corpus_no_dict(corpus_dir, output_directory, 0, False, output_model_path, num_jobs, False)
else:
    benchmark_align_corpus(corpus_dir, dict_path, output_directory, 0, False, output_model_path, num_jobs, True)

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Num_jobs']
if dict_path == None:
        dict_data = [
        {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'tagalog', 'Type of benchmark': 'train and align', 'Total time': benchmark_align_corpus_no_dict[0], 'Num_jobs': num_jobs}
        ]
else:
    dict_data = [
        {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'dog_cat', 'Type of benchmark': 'train and align', 'Total time': benchmark_align_corpus[0], 'Num_jobs': num_jobs}
        ]

now = datetime.now()
date = str(now.year)+str(now.month)+str(now.day)

if not os.path.exists('aligner_benchmark'+date+'.csv'):
    open('aligner_benchmark'+date+'.csv', 'a')
    with open('aligner_benchmark'+date+'.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

csv_file = 'aligner_benchmark'+date+'.csv'

with open('aligner_benchmark'+date+'.csv', 'a') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writerow(dict_data[0])








