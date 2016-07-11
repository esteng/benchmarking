import os
import re
import wave, struct
import librosa
import numpy as np

corpus = os.path.expanduser('/media/share/datasets/aligner_benchmarks/2_French_2000files')

confreeufr = []
confrefr = []
filler = []
senf = []
willf = []
willf2 = []
unused = []
for root, dirs, files in os.walk(corpus):
	for f in files:
		if os.path.exists('quebecfrench/' + f):
			if re.search('confreeufr', f):
				confreeufr.append(f)
			if re.search('confrefr', f):
				confrefr.append(f)
			if re.search('filler', f):
				filler.append(f)
			if re.search('senf', f):
				senf.append(f)
			if re.search('willf', f):
				willf.append(f)
			if re.search('willf2', f):
				willf2.append(f)
subspeaker = []
subjectids = {}
experiments = [confreeufr, confrefr, filler, senf, willf, willf2]
for experiment in experiments:
	for i in experiment:
		dog = i.split('_')
		subid = dog[0] + '_' + dog[1]
		if len(list(dog[2])) == 1:
			cat = re.sub(i, '0' + dog[2] + '_' + dog[3], i)
		else:
			cat = re.sub(i, dog[2] + '_' + dog[3], i)
		if subid not in subjectids:
			subjectids[subid] = [(i, cat)]
		else:
			subjectids[subid].append((i, cat))

if not os.path.exists('/media/share/datasets/aligner_benchmarks/sorted_quebec_french'):
	os.makedirs('/media/share/datasets/aligner_benchmarks/sorted_quebec_french')

for i in subjectids.keys():
	if not os.path.exists('/media/share/datasets/aligner_benchmarks/sorted_quebec_french/' + i):
	   	os.makedirs('/media/share/datasets/aligner_benchmarks/sorted_quebec_french/' + i)
	for j in subjectids[i]:
		os.rename(corpus + '/' + j[0], 'sorted_quebec_french/' + i + '/' + j[1])
