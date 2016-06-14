import time
import os
import logging
import platform
import csv
import statistics
from datetime import datetime

from polyglotdb.exceptions import ConnectionError, NetworkAddressError, TemporaryConnectionError, PGError

from polyglotdb.graph.func import Sum

from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig

import polyglotdb.io as pgio
from polyglotdb.io import (inspect_buckeye, inspect_textgrid, inspect_timit,
                        inspect_labbcat, inspect_mfa, inspect_fave,
                        guess_textgrid_format)
from polyglotdb.io.enrichment import enrich_lexicon_from_csv, enrich_features_from_csv

from polyglotdb.utils import update_sound_files, gp_language_stops, gp_speakers

from polyglotdb.acoustics.analysis import get_pitch, get_formants, acoustic_analysis

graph_db = {'graph_host':'localhost', 'graph_port': 7774,
            'user': 'neo4j', 'password': 'test'}

amountofcorpus = 'full'
#amountofcorpus = 'partial'

buckeye = os.path.expanduser('/media/share/datasets/sct_benchmarks/automated/buckeye')
buckeyebenchmark = 'buckeyebenchmark'

globalphone = os.path.expanduser('/media/share/datasets/sct_benchmarks/automated/globalphone')
globalphonebenchmark = 'globalphonebenchmark'

sotc = os.path.expanduser('/media/share/datasets/sct_benchmarks/automated/sotc')
sotcbenchmark = 'sotcbenchmark'

timit = os.path.expanduser('/media/share/datasets/sct_benchmarks/automated/timit')
timitbenchmark = 'timitbenchmark'

lasttime = time.time()
times = []

def call_back(*args):
    global lasttime
    print(*args)
    if len(args) > 1:
        return
    if isinstance(args[0], int):
        logtime = time.time() - lasttime
        print(logtime)
        times.append(logtime)
        lasttime = time.time()

def import_corpus_run_query(data, path):
    with CorpusContext(data, **graph_db) as c:
        c.reset()
        beg = time.time()
        if data == 'buckeyebenchmark':
            parser = inspect_buckeye(path)
        elif data == 'timitbenchmark':
            parser = inspect_timit(path)
        else:
            form = guess_textgrid_format(path)
            if form == 'labbcat':
                parser = inspect_labbcat(path)
            elif form == 'mfa':
                parser = inspect_mfa(path)
            elif form == 'fave':
                parser = inspect_fave(path)
            else:
                parser = inspect_textgrid(path)
        parser.call_back = call_back
        c.load(parser, path)
        end = time.time()
        avgtime = sum(times)/(len(times))
        sd = statistics.stdev(times)
        return [(end - beg), avgtime, sd]

buckeye_import = import_corpus_run_query(buckeyebenchmark, buckeye)
globalphone_import = import_corpus_run_query(globalphonebenchmark, globalphone)
#sotc_import = import_corpus_run_query(sotcbenchmark, sotc)
timit_import = import_corpus_run_query(timitbenchmark, timit)

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Mean time per call back', 'sd time between call backs']
dict_data = [
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': amountofcorpus + 'buckeye', 'Type of benchmark': 'Import', 'Total time': buckeye_import[0], 'Mean time per call back': buckeye_import[1], 'sd time between call backs': buckeye_import[2]},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': amountofcorpus + 'globalphone', 'Type of benchmark': 'Import', 'Total time': globalphone_import[0], 'Mean time per call back': globalphone_import[1], 'sd time between call backs': globalphone_import[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': amountofcorpus + 'sotc', 'Type of benchmark': 'Import', 'Total time': sotc_import[0], 'Mean time per call back': sotc_import[1], 'sd time between call backs': sotc_import[2]},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': amountofcorpus + 'timit', 'Type of benchmark': 'Import', 'Total time': timit_import[0], 'Mean time per call back': timit_import[1], 'sd time between call backs': timit_import[2]},
    ]

currentPath = os.getcwd()

now = datetime.now()
date = str(now.year)+str(now.month)+str(now.day)

if not os.path.exists('benchmark'+date+'.csv'):
    open('benchmark'+date+'.csv', 'a')

csv_file = 'benchmark'+date+'.csv'

with open('benchmark'+date+'.csv', 'a') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerow(dict_data[0])
    writer.writerow(dict_data[1])
    writer.writerow(dict_data[2])
    #writer.writerow(dict_data[3])
