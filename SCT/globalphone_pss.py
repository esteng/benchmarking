import time
from datetime import datetime
import os
import logging
import platform
import csv
import statistics

from polyglotdb import CorpusContext
from polyglotdb.config import CorpusConfig

from polyglotdb.io import (inspect_buckeye, inspect_textgrid, inspect_timit,
                        inspect_labbcat, inspect_mfa, inspect_fave,
                        guess_textgrid_format)

graph_db = {'graph_host':'localhost', 'graph_port': 7474,
            'user': 'neo4j', 'password': 'test'}

amountofcorpus = 'full'
#amountofcorpus = 'partial'

#globalphonebenchmark = 'globalphonebenchmark'
globalphonebenchmark = 'globalphone_cz'

globalphonesyllabic = ['a', 'aa', 'aw', 'e', 'ee', 'ew', 'i', 'ii', 'o', 'oo', 'ow', 'u', 'uu']

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

def pause_encoding_run_query(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
    	c.encode_pauses('^[<{].*$', call_back=call_back)
    end = time.time()
    if len(times) >1:
    	avgtime = sum(times)/len(times)
    	sd = statistics.stdev(times)
    else:
    	avgtime = times[0]
    	sd = None
    return [(end - beg), avgtime, sd]

def utterance_encoding_run_query(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_utterances(0.5, 0, call_back=call_back)
    end = time.time()
    avgtime = sum(times)/len(times)
    #sd = statistics.stdev(times)
    sd = None
    return [(end - beg), avgtime, sd]

def syllabic_encoding_run_query(data, syllabic):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.reset_class('syllabic')
        c.encode_class(syllabic, 'syllabic')
    end = time.time()
    #avgtime = sum(times)/len(times)
    return [(end - beg), None]

def syllable_encoding_run_query(data):
    beg = time.time()
    algorithm = 'maxonset'
    with CorpusContext(data, **graph_db) as c:
        c.encode_syllables(algorithm = algorithm)
    end = time.time()
    return [(end - beg), None]

def speech_rate_phones(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('utterance', 'phone', 'speech_rate_phones')
    end = time.time()
    return [(end-beg), None]

def speech_rate_syllables(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('utterance', 'syllable', 'speech_rate_syllables')
    end = time.time()
    return [(end-beg), None]

def number_of_syllables(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('word', 'syllable', 'number_of_syllables')
    end = time.time()
    return [(end-beg), None]

def number_of_phones(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('syllable', 'phone', 'number_of_phones')
    end = time.time()
    return [(end-beg), None]

def position_in_utterance(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('utterance', 'word', 'number_of_phones')
    end = time.time()
    return [(end-beg), None]

def position_in_word(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_rate('word', 'syllable', 'number_of_phones')
    end = time.time()
    return [(end-beg), None]

def export_query_pss(data, export_path):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        print (c.hierarchy.token_properties)
        print (c.hierarchy.type_properties)
        '''query = c.query_graph(c.syllable)
        filters = (c.syllable.word.end == c.syllable.word.utterance.end)
        query = query.filter(filters)
        columns = (c.syllable.word.label, c.syllable.word.duration, c.syllable.word.begin, c.syllable.word.end,
            c.syllable.word.number_of_syllables, c.syllable.word.position_in_utterance,
            c.pause.following.duration, c.pause.following.label,
            c.syllable.utterance.speech_rate_phones, c.syllable.utterance.speech_rate_syllable, c.syllable.utterance.begin,
            c.syllable.utterance.end, c.syllable.utterance.number_of_words,
            c.syllable.discourse, c.syllable.speaker,
            c.syllable.duration, c.syllable.label, c.syllable.position_in_word, c.syllable.number_of_phones)
        query = query.columns(*columns)
        print (query.cypher())
        results = query.to_csv(export_path)'''
    end = time.time()
    return [(end-beg)]

#globalphone_pauses = pause_encoding_run_query(globalphonebenchmark)
#globalphone_utts = utterance_encoding_run_query(globalphonebenchmark)
#globalphone_syllabic = syllabic_encoding_run_query(globalphonebenchmark, globalphonesyllabic)
#globalphone_syllables = syllable_encoding_run_query(globalphonebenchmark)
#globalphone_speechrate_phones = speech_rate_phones(globalphonebenchmark)
#globalphone_speechrate_syllables = speech_rate_syllables(globalphonebenchmark)
globalphone_num_syllables = number_of_syllables(globalphonebenchmark)
globalphone_num_phones = number_of_phones(globalphonebenchmark)
globalphone_word_position = position_in_utterance(globalphonebenchmark)
globalphone_syllable_position = position_in_word(globalphonebenchmark)
#globalphone_export_pss = export_query_pss(globalphonebenchmark, 'exportbenchmark.csv')

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Mean time per call back', 'sd time between call backs']
dict_data = [
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Pause encoding', 'Total time': globalphone_pauses[0], 'Mean time per call back': globalphone_pauses[1], 'sd time between call backs': globalphone_pauses[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Utterance encoding', 'Total time': globalphone_utts[0], 'Mean time per call back': globalphone_utts[1], 'sd time between call backs': globalphone_utts[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllabic encoding', 'Total time': globalphone_syllabic[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable encoding', 'Total time': globalphone_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (phones)', 'Total time': globalphone_speechrate_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (syllables)', 'Total time': globalphone_speechrate_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num syllables encoding', 'Total time': globalphone_num_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num phones encoding', 'Total time': globalphone_num_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Word position encoding', 'Total time': globalphone_word_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable position encoding', 'Total time': globalphone_syllable_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Export polysyllabic shortening', 'Total time': globalphone_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
    ]

now = datetime.now()
date = str(now.year)+str(now.month)+str(now.day)

if not os.path.exists('benchmark'+date+'.csv'):
    open('benchmark'+date+'.csv', 'a')
    with open('benchmark'+date+'.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

csv_file = 'benchmark'+date+'.csv'

with open('benchmark'+date+'.csv', 'a') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writerow(dict_data[0])
    writer.writerow(dict_data[1])
    writer.writerow(dict_data[2])
    writer.writerow(dict_data[3])
    #writer.writerow(dict_data[4])
    #writer.writerow(dict_data[5])


