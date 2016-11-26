import sys
import shutil, os
sys.path.insert(0, os.path.expanduser('/data/mmcauliffe/dev/Montreal-Forced-Aligner'))

import time
import logging
import platform
import csv
import statistics
from datetime import datetime

from aligner.command_line.train_and_align import align_corpus, align_corpus_no_dict

corpus_dir = '/data/mmcauliffe/data/LibriSpeech'
dict_path = os.path.expanduser('/data/mmcauliffe/data/LibriSpeech/librispeech-lexicon.txt')
output_directory = '/data/mmcauliffe/aligner-output/LibriSpeech'
output_model_path = os.path.expanduser('/data/mmcauliffe/aligner-models/librispeech_models.zip')
temp_dir = '/data/mmcauliffe/temp/MFA'
num_jobs = 12

def benchmark_align_corpus(corpus_dir, dict_path, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose):
    beg = time.time()
    align_corpus(corpus_dir, dict_path, output_directory, temp_dir, speaker_characters,fast,
            output_model_path, num_jobs, verbose, False)
    end = time.time()
    return [(end - beg)]

def benchmark_align_corpus_no_dict(corpus_dir, output_directory, speaker_characters, fast,
            output_model_path, num_jobs, verbose):
    beg = time.time()
    align_corpus_no_dict(corpus_dir, output_directory, temp_dir, speaker_characters, fast,
            output_model_path, num_jobs, verbose, False)
    end = time.time()
    return [(end - beg)]

if dict_path == None:
    nodict = benchmark_align_corpus_no_dict(corpus_dir, output_directory, 0, False, output_model_path, num_jobs, True)
else:
    yesdict = benchmark_align_corpus(corpus_dir, dict_path, output_directory, 0, False, output_model_path, num_jobs, True)

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
        {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': corpus_dir, 'Type of benchmark': 'train and align', 'Total time': nodict[0], 'Num_jobs': num_jobs}
        ]
else:
    dict_data = [
        {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': corpus_dir, 'Type of benchmark': 'train and align', 'Total time': yesdict[0], 'Num_jobs': num_jobs}
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


