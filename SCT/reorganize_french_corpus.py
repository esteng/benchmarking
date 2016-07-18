import os
import re
import wave, struct
import librosa
import numpy as np
import subprocess

new_sr = 22050

corpus = os.path.expanduser('/media/share/datasets/aligner_benchmarks/sorted_quebec_french')

henrison = []
'''ampp = []
apchk = []
cas2 = []
cas4 = []
chess = []
enco = []
ersapro9 = []
fogea = []
give_prod = []
inc = []
incfast = []
mrbr = []
npgi = []
npgi2 = []
npgi4 = []
nvp2 = []
RFRcontour = []
rnrp = []
sco = []
scoinPro = []
scoinPro2 = []
socr = []
socrLo = []
syse6 = []
syse7 = []
syse8 = []
other = []
unused = []'''

'''for root, dirs, files in os.walk(corpus):
	for f in files:
		if os.path.exists(corpus + '/' + f):
			if re.search('henrison', f):
				henrison.append(f)
			if re.search('ampp', f):
				ampp.append(f)
			elif re.search('apchk', f):
				apchk.append(f)
			elif re.search('cas2', f):
				cas2.append(f)
			elif re.search('cas4', f):
				cas4.append(f)
			elif re.search('chess', f):
				chess.append(f)
			elif re.search('enco', f):
				enco.append(f)
			elif re.search('ersapro9', f):
				ersapro9.append(f)
			elif re.search('fogea', f):
				fogea.append(f)
			elif re.search('give-prod', f):
				give_prod.append(f)
			elif re.search('inc', f):
				inc.append(f)
			elif re.search('incfast', f):
				incfast.append(f)
			elif re.search('mrbr', f):
				mrbr.append(f)
			elif re.search('npgi', f):
				npgi.append(f)
			elif re.search('npgi2', f):
				npgi2.append(f)
			elif re.search('npgi4', f):
				npgi4.append(f)				
			elif re.search('nvp2', f):
				nvp2.append(f)
			elif re.search('RFRcontour', f):
				RFRcontour.append(f)
			elif re.search('rnrp', f):
				rnrp.append(f)
			elif re.search('sco', f):
				sco.append(f)
			elif re.search('scoinPro', f):
				scoinPro.append(f)
			elif re.search('scoinPro2', f):
				scoinPro2.append(f)
			elif re.search('socr', f):
				socr.append(f)
			elif re.search('socrLo', f):
				socrLo.append(f)
			elif re.search('syse6', f):
				syse6.append(f)
			elif re.search('syse7', f):
				syse7.append(f)
			elif re.search('syse8', f):
				syse8.append(f)
			else:
				other.append(f)'''
subspeaker = []
subjectids = {}
experiments = [henrison]
'''[ampp, apchk, cas2, cas4, chess, enco, ersapro9, fogea, give_prod, inc, incfast, 
mrbr, npgi, npgi2, npgi4, nvp2, RFRcontour, rnrp, sco, scoinPro, scoinPro2, socr, socrLo, 
syse6, syse7, syse8]'''
'''for experiment in experiments:
	for i in experiment:
		dog = i.split('_')
		subid = dog[0] + '_' + dog[1]
		if len(list(dog[2])) == 1:
			cat = re.sub(i, '0' + dog[2] + '_' + dog[3], i)
		elif len(list(dog[2])) == 2:
			cat = re.sub(i, dog[2] + '_' + dog[3], i)
		if subid not in subjectids:
			subjectids[subid] = [(i, cat)]
		else:
			subjectids[subid].append((i, cat))'''
'''for i in other:
	dog = i.split('.')
	subid = dog[0]
	cat = '01_1.' + dog[1]
	if subid not in subjectids:
		subjectids[subid] = [(i, cat)]
	else:
		subjectids[subid].append((i, cat))'''

'''if not os.path.exists('/media/share/datasets/aligner_benchmarks/sorted_tagalog'):
	os.makedirs('/media/share/datasets/aligner_benchmarks/sorted_tagalog')
for i in subjectids.keys():
	if not os.path.exists('/media/share/datasets/aligner_benchmarks/sorted_tagalog/' + i):
	   	os.makedirs('/media/share/datasets/aligner_benchmarks/sorted_tagalog/' + i)
	for j in subjectids[i]:
		try:
			os.rename(corpus + '/' + j[0], '/media/share/datasets/aligner_benchmarks/sorted_tagalog/' + i + '/' + j[1])
		except:
			pass'''

for root, dirs, files in os.walk(corpus):
    for f in files:
        filepath = os.path.join(root, f)
        subprocess.call(['sox', filepath.replace('\\','/'), filepath.replace('\\','/'),
                        'gain', '-1', 'rate', '-I', str(new_sr)])




