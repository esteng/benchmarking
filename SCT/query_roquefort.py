import time
from datetime import datetime
import os
import logging
import platform
import csv
import statistics

from polyglotdb import CorpusContext

graph_db = {'graph_host':'roquefort.linguistics.mcgill.ca', 'graph_port': 7474,
            'user': 'neo4j', 'password': 'test'}

lang = 'vn'

with CorpusContext('globalphone_{}'.format(lang), **graph_db) as c:
    c.refresh_hierarchy()
    print(c.hierarchy._data)
    c.encode_count('word', 'phone', 'number_of_phones')
    syl = c.phone.subset_type('syllabic')
    query = c.query_graph(syl)
    query = query.filter(c.phone.syllable.word.end == c.phone.utterance.end)
    columns = (syl.word.id.column_name('word_id'),
        syl.label.column_name('nucleus'),
        syl.duration.column_name('vowel_duration'),
        syl.word.number_of_phones.column_name('num_phones_in_word'),
        syl.word.label.column_name('orthography'),
        syl.word.duration.column_name('word_duration'),
        syl.word.begin.column_name('word_begin'),
        syl.word.end.column_name('word_end'),
        syl.word.number_of_syllables.column_name('num_syllables_in_word'),
        syl.word.position_in_utterance.column_name('position_in_utterance'),
        syl.utterance.speech_rate_phones.column_name('speech_rate_phones'),
        syl.utterance.speech_rate_syllables.column_name('speech_rate_syllables'),
        syl.utterance.begin.column_name('utterance_begin'),
        syl.utterance.end.column_name('utterance_end'),
        syl.utterance.number_of_words.column_name('num_words'),
        syl.discourse.name.column_name('discourse_name'),
        syl.speaker.name.column_name('speaker_name'),
        syl.syllable.duration.column_name('syllable_duration'),
        syl.syllable.label.column_name('syllable_label'),
        syl.syllable.position_in_word.column_name('syllable_position'),
        syl.syllable.number_of_phones.column_name('num_phones_in_syllable'))

    print (query.cypher())
    query = query.columns(*columns)
    print (query.cypher())
    results = query.to_csv('{}.csv'.format(lang))

