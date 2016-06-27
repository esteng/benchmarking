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

#globalphonesyllabic = ['a', 'aa', 'aw', 'e', 'ee', 'ew', 'i', 'ii', 'o', 'oo', 'ow', 'u', 'uu']#cz
#globalphonesyllabic = ['ab', 'e', 'i', 'i2', 'o', 'oe', 'u', 'ue']#tu
globalphonesyllabic = ['a', 'e', 'i', 'o', 'u']#sa

globalphone = os.path.expanduser('/media/share/corpora/GP_aligned/CZ')
lang = 'cz'

outpath = 'exportbenchmark_cz.csv'

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
            parser = inspect_mfa(path)
        parser.call_back = call_back
        c.load(parser, path)
        end = time.time()
        avgtime = sum(times)/(len(times))
        sd = statistics.stdev(times)
        return [(end - beg), avgtime, sd]

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
        c.encode_count('word', 'syllable', 'number_of_syllables')
    end = time.time()
    return [(end-beg), None]

def number_of_phones(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_count('syllable', 'phone', 'number_of_phones')
    end = time.time()
    return [(end-beg), None]

def number_of_words(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_count('utterance', 'word', 'number_of_words')
    end = time.time()
    return [(end-beg), None]

def position_in_utterance(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_position('utterance', 'word', 'position_in_utterance')
    end = time.time()
    return [(end-beg), None]

def position_in_word(data):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        c.encode_position('word', 'syllable', 'position_in_word')
    end = time.time()
    return [(end-beg), None]

def export_query_pss(data, export_path):
    beg = time.time()
    with CorpusContext(data, **graph_db) as c:
        #print (c.hierarchy.token_properties)
        #print (c.hierarchy.type_properties)
        query = c.query_graph(c.syllable)
        filters = (c.syllable.word.end == c.syllable.word.utterance.end)
        query = query.filter(filters)
        columns = (c.syllable.word.id.column_name('word_id'), c.syllable.word.label.column_name('orthography'), c.syllable.word.duration.column_name('word_duration'), c.syllable.word.begin.column_name('word_begin'), c.syllable.word.end.column_name('word_end'),
            c.syllable.word.number_of_syllables.column_name('num_syllables_in_word'), c.syllable.word.position_in_utterance.column_name('position_in_utterance'),
            c.pause.following.duration.column_name('following_pause_duration'), c.pause.following.label.column_name('following_pause_label'),
            c.syllable.utterance.speech_rate_phones.column_name('speech_rate_phones'), c.syllable.utterance.speech_rate_syllables.column_name('speech_rate_syllables'), c.syllable.utterance.begin.column_name('utterance_begin'),
            c.syllable.utterance.end.column_name('utterance_end'), c.syllable.utterance.number_of_words.column_name('num_words'),
            c.syllable.discourse.name.column_name('discourse_name'), c.syllable.speaker.name.column_name('speaker_name'),
            c.syllable.duration.column_name('syllable_duration'), c.syllable.label.column_name('syllable_label'), c.syllable.position_in_word.column_name('syllable_position'), c.syllable.number_of_phones.column_name('num_phones_in_syllable'))

        query = query.columns(*columns)
        print (query.cypher())
        results = query.to_csv(export_path)
    end = time.time()
    return [(end-beg)]

#globalphone_import = import_corpus_run_query(globalphonebenchmark, globalphone)

#globalphone_import = import_corpus_run_query(globalphonebenchmark, globalphone)
#globalphone_pauses = pause_encoding_run_query(globalphonebenchmark)
#globalphone_utts = utterance_encoding_run_query(globalphonebenchmark)
#globalphone_syllabic = syllabic_encoding_run_query(globalphonebenchmark, globalphonesyllabic)
#globalphone_syllables = syllable_encoding_run_query(globalphonebenchmark)
#globalphone_speechrate_phones = speech_rate_phones(globalphonebenchmark)
#globalphone_speechrate_syllables = speech_rate_syllables(globalphonebenchmark)
#globalphone_num_syllables = number_of_syllables(globalphonebenchmark)
#globalphone_num_phones = number_of_phones(globalphonebenchmark)
#globalphone_num_words = number_of_words(globalphonebenchmark)
#globalphone_word_position = position_in_utterance(globalphonebenchmark)
#globalphone_syllable_position = position_in_word(globalphonebenchmark)
globalphone_export_pss = export_query_pss(globalphonebenchmark, outpath)

def WriteDictToCSV(csv_file,csv_columns,dict_data):
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)   
        return            

csv_columns = ['Computer','Date','Corpus', 'Type of benchmark', 'Total time', 'Mean time per call back', 'sd time between call backs']
dict_data = [
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': amountofcorpus + globalphonebenchmark, 'Type of benchmark': 'Import', 'Total time': globalphone_import[0], 'Mean time per call back': globalphone_import[1], 'sd time between call backs': globalphone_import[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Pause encoding', 'Total time': globalphone_pauses[0], 'Mean time per call back': globalphone_pauses[1], 'sd time between call backs': globalphone_pauses[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Utterance encoding', 'Total time': globalphone_utts[0], 'Mean time per call back': globalphone_utts[1], 'sd time between call backs': globalphone_utts[2]},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllabic encoding', 'Total time': globalphone_syllabic[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable encoding', 'Total time': globalphone_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (phones)', 'Total time': globalphone_speechrate_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (syllables)', 'Total time': globalphone_speechrate_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num syllables encoding', 'Total time': globalphone_num_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num phones encoding', 'Total time': globalphone_num_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num words encoding', 'Total time': globalphone_num_words[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Word position encoding', 'Total time': globalphone_word_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
    #{'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable position encoding', 'Total time': globalphone_syllable_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Export polysyllabic shortening', 'Total time': globalphone_export_pss[0], 'Mean time per call back': None, 'sd time between call backs': None},
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
    #writer.writerow(dict_data[1])
    #writer.writerow(dict_data[2])
    #writer.writerow(dict_data[3])
    #writer.writerow(dict_data[4])
    #writer.writerow(dict_data[5])


