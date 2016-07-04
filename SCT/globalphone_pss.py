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

globalphonebenchmark = 'globalphone_sw'
#globalphonebenchmark = 'timitbenchmark'

#globalphonesyllabic = ['a', 'aa', 'aw', 'e', 'ee', 'ew', 'i', 'ii', 'o', 'oo', 'ow', 'u', 'uu']#cz
#globalphonesyllabic = ['ab', 'e', 'i', 'i2', 'o', 'oe', 'u', 'ue']#tu
#globalphonesyllabic = ['a', 'e', 'i', 'o', 'u']#sa
#globalphonesyllabic = ['i', 'y', 'u', 'e', 'EU', 'o', 'E', 'OE', 'AX', 'O', 'a', 'AE', 'A~', 'E~', 'o~', 'OE~']#fr
globalphonesyllabic = ['a', 'ae', 'ale', 'e', 'etu', 'i', 'o', 'oc', 'oe', 'ole', 'ox', 'u', 'ue', 'abl', 'ael', 'al',
        'alel', 'el', 'il', 'oel', 'ole', 'olel', 'uel', 'ul', 'uxl']#sw
#globalphonesyllabic = ['a', 'ae', 'atu', 'e', 'etu', 'i', 'o', 'oe', 'u', 'ue', 'aI', 'aU', 'eU', 'al', 'el', 'il',
 #       'oel', 'ol', 'uel', 'ul']#ge
#globalphonesyllabic = ['a', 'y', 'e', 'i', 'o', 'u', 'ja', 'ju']#bg
#globalphonesyllabic = ['a', 'e', 'i', 'o', 'u', 'a_L', 'e_L', 'i_L', 'o_L', 'u_L', 'a_T1', 'e_T1', 'i_T1', 'o_T1', 'u_T1',
 #       'a_T2', 'e_T2', 'i_T2', 'o_T2', 'u_T2', 'a_T3', 'e_T3', 'i_T3', 'o_T3', 'u_T3', 'aI', 'aU']#ha
#globalphonesyllabic = ['a', 'e', 'i', 'i2', 'o', 'u', 'jA', 'jE', 'jO', 'jU']#ru
#globalphonesyllabic = ['a', 'e', 'eo5', 'i', 'i2', 'o', 'oc5', 'u']#pl
#globalphonesyllabic = ['A', 'AX', 'A~', 'E', 'E~', 'I', 'IX', 'I~', 'O', 'O~', 'U', 'UX', 'U~', 'A+', 'A~+',
 #       'E+', 'E~+', 'O+', 'O~+', 'U+', 'U~+', 'I+', 'I~+']#po
#globalphonesyllabic = ['a', 'e', 'i', 'o', 'u', 'y']#ua
#globalphonesyllabic = ['A', 'EO', 'O', 'U', 'I', 'EU', 'AE', 'E', 'OE', 'UE', 'iA', 'iEO', 'iO', 'iU', 'iE', 'oA', 'uEO', 'eul']#ko
#globalphonesyllabic = ['a1', 'a2', 'a3', 'e1', 'e2', 'i', 'o1', 'o2', 'o3', 'u1', 'u2', 'ai', 'ao', 'au', 'au3',
 #       'ay', 'ay3', 'eo', 'eu', 'ie2', 'iu', 'oa', 'oe', 'oi', 'oi2', 'oi3', 'ua', 'ua2', 'ui', 'ui2', 'uu2', 'uy', 'ieu',
 #       'uoi2', 'uoi3', 'uou']#vn
#globalphonesyllabic = ['a1', 'a2', 'a3', 'a4', 'a5', 'ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ao1', 'ao2', 'ao3', 'ao4', 'ao5',
 #       'e1', 'e2', 'e3', 'e4', 'e5', 'ei1', 'ei2', 'ei3', 'ei4', 'ei5', 'i1', 'i2', 'i3', 'i4', 'i5',
 #       'ia1', 'ia2', 'ia3', 'ia4', 'ia5', 'ie1', 'ie2', 'ie3', 'ie4', 'ie5', 'ii1', 'ii2', 'ii3', 'ii4', 'ii5',
 #       'io1', 'io2', 'io3', 'io4', 'io5', 'iu1', 'iu2', 'iu3', 'iu4', 'iu5', 'o1', 'o2', 'o3', 'o4', 'o5',
 #       'ou1', 'ou2', 'ou3', 'ou4', 'ou5', 'u1', 'u2', 'u3', 'u4', 'u5', 'ua1', 'ua2', 'ua3', 'ua4', 'ua5',
 #       'ue1', 'ue2', 'ue3', 'ue4', 'ue5', 'uo1', 'uo2', 'uo3', 'uo4', 'uo5',   
 #       'v1', 'v2', 'v3', 'v4', 'v5', 'va1', 'va2', 'va3', 'va4', 've1', 've2', 've3', 've4',
 #       'iao1', 'iao2', 'iao3', 'iao4', 'iao5', 'iou1', 'iou2', 'iou3', 'iou4', 'uai1', 'uai2', 'uai3', 'uai4', 'uai5',
 #       'uei1', 'uei2', 'uei3', 'uei4', 'uei5',]#ch
#globalphonesyllabic = ['AA0', 'AE0', 'AH0', 'AO0', 'AW0', 'AY0', 'EH0', 'ER0', 'EY0', 'IH0', 'IY0', 'OW0', 'OY0', 'UH0', 'UW0', 
 #       'AA1', 'AE1', 'AH1', 'AO1', 'AW1', 'AY1', 'EH1', 'ER1', 'EY1', 'IH1', 'IY1', 'OW1', 'OY1', 'UH1', 'UW1',
 #       'AA2', 'AE2', 'AH2', 'AO2', 'AW2', 'AY2', 'EH2', 'ER2', 'EY2', 'IH2', 'IY2', 'OW2', 'OY2', 'UH2', 'UW2']#librispeech
#globalphonesyllabic = ['aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'ax-h', 'axr', 'ay',
 #           'eh', 'el', 'em', 'en', 'eng', 'er', 'ey', 'ih', 'ix', 'iy', 'ow',' oy', 'uh', 'uw', 'ux']#timit

globalphone = os.path.expanduser('/media/share/corpora/GP_aligned/SW')
#globalphone = os.path.expanduser('/media/share/datasets/sct_benchmarks/LibriSpeech')
#globalphone = os.path.expanduser('/media/share/datasets/sct_benchmarks/automated/timit')
lang = 'sw'

outpath = 'export_sw.csv'

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
        #pattern = '^[<{].*$'
        #if 'timit' in data:
        # pattern = '^<?(sil|SIL)>?$'
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
        c.encode_syllables(algorithm = algorithm, call_back=call_back)
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
        c.refresh_hierarchy()
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
globalphone_syllables = syllable_encoding_run_query(globalphonebenchmark)
globalphone_speechrate_phones = speech_rate_phones(globalphonebenchmark)
globalphone_speechrate_syllables = speech_rate_syllables(globalphonebenchmark)
globalphone_num_syllables = number_of_syllables(globalphonebenchmark)
globalphone_num_phones = number_of_phones(globalphonebenchmark)
globalphone_num_words = number_of_words(globalphonebenchmark)
globalphone_word_position = position_in_utterance(globalphonebenchmark)
globalphone_syllable_position = position_in_word(globalphonebenchmark)
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
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable encoding', 'Total time': globalphone_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (phones)', 'Total time': globalphone_speechrate_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Speech rate encoding (syllables)', 'Total time': globalphone_speechrate_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num syllables encoding', 'Total time': globalphone_num_syllables[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num phones encoding', 'Total time': globalphone_num_phones[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Num words encoding', 'Total time': globalphone_num_words[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Word position encoding', 'Total time': globalphone_word_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
    {'Computer': platform.node(), 'Date': str(datetime.now()), 'Corpus': globalphonebenchmark, 'Type of benchmark': 'Syllable position encoding', 'Total time': globalphone_syllable_position[0], 'Mean time per call back': None, 'sd time between call backs': None},
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
    writer.writerow(dict_data[1])
    writer.writerow(dict_data[2])
    writer.writerow(dict_data[3])
    writer.writerow(dict_data[4])
    writer.writerow(dict_data[5])
    writer.writerow(dict_data[6])
    writer.writerow(dict_data[7])
    writer.writerow(dict_data[8])
    #writer.writerow(dict_data[9])
    #writer.writerow(dict_data[10])
    #writer.writerow(dict_data[11])
    #writer.writerow(dict_data[12])


