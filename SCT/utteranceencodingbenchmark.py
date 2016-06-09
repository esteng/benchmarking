import time
import os
import logging
import platform
from datetime import datetime
import csv
import statistics

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

csvinfo = []

graph_db = {'graph_host':'localhost', 'graph_port': 7774,
            'user': 'neo4j', 'password': 'test'}

buckeyebenchmark = 'buckeyebenchmark'
globalphonebenchmark = 'globalphonebenchmark'
sotcbenchmark = 'sotcbenchmark'
timitbenchmark = 'timitbenchmark'

lasttime = time.time()
times = []
times2 = []

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

def utterance_encoding_run_query(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_utterances(0.15, 0, call_back=call_back)
    end = time.time()
    avgtime = sum(times)/len(times)
    sd = statistics.stdev(times)
    return [(end - beg), avgtime, sd]

buckeye_utts = utterance_encoding_run_query(buckeyebenchmark)
globalphone_utts = utterance_encoding_run_query(globalphonebenchmark)
sotc_utts = utterance_encoding_run_query(sotcbenchmark)
timit_utts = utterance_encoding_run_query(timitbenchmark)

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Mean time per call back', 'sd time between call backs']
dict_data = [
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'buckeye', 'Type of benchmark': 'Utterance encoding', 'Total time': buckeye_utts[0], 'Mean time per call back': buckeye_utts[1], 'sd time between call backs': buckeye_utts[2]},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'globalphone', 'Type of benchmark': 'Utterance encoding', 'Total time': globalphone_utts[0], 'Mean time per call back': globalphone_utts[1], 'sd time between call backs': globalphone_utts[2]},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'sotc', 'Type of benchmark': 'Utterance encoding', 'Total time': sotc_utts[0], 'Mean time per call back': sotc_utts[1], 'sd time between call backs': sotc_utts[2]},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'timit', 'Type of benchmark': 'Utterance encoding', 'Total time': timit_utts[0], 'Mean time per call back': timit_utts[1], 'sd time between call backs': timit_utts[2]},
    ]

currentPath = os.getcwd()

if not os.path.exists('benchmark.csv'):
	open('benchmark.csv', 'a')

csv_file = 'benchmark.csv'

with open('benchmark.csv', 'a') as csv_file:
	writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
	writer.writerow(dict_data[0])
	writer.writerow(dict_data[1])
	writer.writerow(dict_data[2])
	writer.writerow(dict_data[3])


