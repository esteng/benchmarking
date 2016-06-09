import time
import os
import logging
import platform
import statistics
import csv
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

graph_db = {'host':'localhost', 'port': 7774,
            'user': 'neo4j', 'password': 'test'}

buckeyebenchmark = 'buckeyebenchmark'
globalphonebenchmark = 'globalphonebenchmark'
sotcbenchmark = 'sotcbenchmark'
timitbenchmark = 'timitbenchmark'

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

if not os.path.exists('exportbenchmark.csv'):
	open('exportbenchmark.csv', 'w')

def export_query_phonetype(data, syllabic, export_path):
    beg = time.time()

    with CorpusContext(data, **graph_db) as c:
    	query = c.query_graph(c.phone)
    	filters = (c.phone.label == syllabic)
    	query = query.filter(filters)
    	columns = (c.phone.label, c.phone.word.label, c.phone.begin, c.phone.end)
    	query = query.columns(*columns)
    	print (query.cypher())
    	results = query.to_csv(export_path)
    end = time.time()
    return [(end-beg)]

def export_query_wfc(data, export_path):
    beg = time.time()

    with CorpusContext(data, **graph_db) as c:
    	query = c.query_graph(c.phone)
    	filters = (c.phone.type_subset == 'consonantal', c.phone.previous.type_subset == 'consonantal', c.phone.end == c.phone.word.end)
    	query = query.filter(*filters)
    	columns = (c.phone.label, c.phone.word.label.column_name('word_orthography'), c.phone.word.duration, c.phone.duration, c.phone.syllable.duration) #c.phone.utterance.speech_rate)
    	query = query.columns(*columns)
    	print (query.cypher())
    	results = query.to_csv(export_path)
    end = time.time()
    return [(end-beg)]

def export_query_pss(data, export_path):
    beg = time.time()

    with CorpusContext(data, **graph_db) as c:
    	query = c.query_graph(c.syllable)
    	filters = (c.syllable.begin == c.syllable.word.begin, c.syllable.word.end == c.syllable.word.utterance.end)#c.syllable.word.stress_pattern == '^#1.*')
    	query = query.filter(*filters)
    	columns = (c.syllable.word.label, c.syllable.discourse, c.syllable.speaker, c.syllable.duration, c.syllable.begin, c.syllable.end)
    	query = query.columns(*columns)
    	print (query.cypher())
    	results = query.to_csv(export_path)
    end = time.time()
    return [(end-beg)]

buckeye_export_pt = export_query_phonetype(buckeyebenchmark, 'aa', 'exportbenchmark.csv')
globalphone_export_pt = export_query_phonetype(globalphonebenchmark, 'i', 'exportbenchmark.csv')
sotc_export_pt = export_query_phonetype(sotcbenchmark, 'I', 'exportbenchmark.csv')
#timit_export_pt = export_query_phonetype(timitbenchmark, 'aa', 'exportbenchmark.csv')


#buckeye_export_wfv = export_query_wfc(buckeyebenchmark, 'exportbenchmark.csv')
globalphone_export_wfv = export_query_wfc(globalphonebenchmark, 'exportbenchmark.csv')
#sotc_export_wfv = export_query_wfc(sotcbenchmark, 'exportbenchmark.csv')
#timit_export_wfv = export_query_wfc(timitbenchmark, 'exportbenchmark.csv')

buckeye_export_pss = export_query_pss(buckeyebenchmark, 'exportbenchmark.csv')
globalphone_export_pss = export_query_pss(globalphonebenchmark, 'exportbenchmark.csv')
sotc_export_pss = export_query_pss(sotcbenchmark, 'exportbenchmark.csv')
#timit_export_pss = export_query_pss(timitbenchmark, 'exportbenchmark.csv')

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Mean time per call back', 'sd time between call backs']
dict_data = [
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'buckeye', 'Type of benchmark': 'Export encoding phonetype', 'Total time': buckeye_export_pt[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'buckeye', 'Type of benchmark': 'Export encoding wordfinalvowels', 'Total time': buckeye_export_wfv[0], 'Mean time per call back': None, 'sd time between call backs': None},
	{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'buckeye', 'Type of benchmark': 'Export encoding pss', 'Total time': buckeye_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'globalphone', 'Type of benchmark': 'Export encoding phonetype', 'Total time': globalphone_export_pt[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'globalphone', 'Type of benchmark': 'Export encoding wordfinalvowels', 'Total time': globalphone_export_wfv[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'globalphone', 'Type of benchmark': 'Export encoding pss', 'Total time': globalphone_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'sotc', 'Type of benchmark': 'Export encoding phonetype', 'Total time': sotc_export_pt[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'sotc', 'Type of benchmark': 'Export encoding wordfinalvowels', 'Total time': sotc_export_wfv[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'sotc', 'Type of benchmark': 'Export encoding pss', 'Total time': sotc_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'timit', 'Type of benchmark': 'Export encoding phonetype', 'Total time': timit_export_pt[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'timit', 'Type of benchmark': 'Export encoding wordfinalvowels', 'Total time': timit_export_wfv[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': 'timit', 'Type of benchmark': 'Export encoding pss', 'Total time': timit_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
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
	writer.writerow(dict_data[4])
	writer.writerow(dict_data[5])
	writer.writerow(dict_data[6])
	#writer.writerow(dict_data[7])
	#writer.writerow(dict_data[8])
	#writer.writerow(dict_data[9])
	#writer.writerow(dict_data[10])
	#writer.writerow(dict_data[11])



