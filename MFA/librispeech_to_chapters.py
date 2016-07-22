import os
import re
import wave, struct
import librosa
import numpy as np

from scipy.io import wavfile
from textgrid import TextGrid, IntervalTier

chapters = []
textgrids = []
wavfiles = []
labfiles = []
chap_to_speak = {}
for root, dirs, files in os.walk('LibriSpeech/908'):
	for f in files:
		#if not (f.endswith('.TextGrid') or f.endswith('.wav')):
		#	continue
		name, ext = os.path.splitext(f)
		speaker, chapternum, frag = name.split('-')
		chap_to_speak[chapternum] = speaker
		if len(chapternum) > 0 and chapternum not in chapters:
			chapters.append(chapternum)
		if re.search('TextGrid', f):
			textgrids.append(os.path.join(root, f))
		if re.search('wav', f):
			wavfiles.append(os.path.join(root,f))
		if re.search('lab', f):
			labfiles.append(os.path.join(root,f))

def load_textgrid(path):
    tg = TextGrid()
    try:
        tg.read(path)
    except ValueError as e:
        print('The file {} could not be parsed: {}'.format(path, str(e)))
    return tg

if not os.path.exists('chapterswithphones'):
    os.makedirs('chapterswithphones')

if not os.path.exists('chapterswithtext'):
	os.makedirs('chapterswithtext')

for chapter in chapters:
	speaker = chap_to_speak[chapter]
	if not os.path.exists('chapterswithphones' + '/' + speaker):
		os.makedirs('chapterswithphones' + '/' + speaker)
	if not os.path.exists('chapterswithtext' + '/' + speaker):
		os.makedirs('chapterswithtext' + '/' + speaker)

	wavfileoutpath = 'chapterswithphones' + '/' + speaker + '/' + chapter + '.wav'
	groupedwavfiles = []
	wavfiletimes = []
	for w in wavfiles:
		if re.search(chapter, w):
			groupedwavfiles.append(w)
	signal = None
	duration = 0
	for p in groupedwavfiles:
		s, sr = librosa.load(p, sr = None)
		s *= 32768
		if signal is None:
			signal = s
		else:
			signal = np.append(signal, s)
		wfile = wave.open(p, 'r')
		time = (1.0 * wfile.getnframes ()) / wfile.getframerate ()
		duration += time
		wavfiletimes.append(duration)
	wavfile.write(wavfileoutpath, sr, signal.astype('int16'))

	groupedlabfiles = []
	groupedlabtext = []
	for w in labfiles:
		if re.search(chapter, w):
			groupedlabfiles.append(w)
	for p in groupedlabfiles:
		f = open(p, 'r')
		text = f.read()
		groupedlabtext.append(text)

	chapteroutpath1 = 'chapterswithphones' + '/' + speaker + '/' + chapter + '.TextGrid'
	chapteroutpath2 = 'chapterswithtext' + '/' + speaker + '/' + chapter + '.TextGrid'
	groupedtextgrids = []
	for tg in textgrids:
		if re.search(chapter, tg):
			groupedtextgrids.append(tg)
	wordintervals = []
	phoneintervals = []
	cur_dur = 0
	for t in groupedtextgrids:
		tg = load_textgrid(t)
		maxtime = tg.maxTime
		for i, ti in enumerate(tg.tiers):
			if i == 0:
				for x in ti:
					x.maxTime += cur_dur
					x.minTime += cur_dur
					wordintervals.append(x)

			elif i == 1:
				for x in ti:
					x.maxTime += cur_dur
					x.minTime += cur_dur
					phoneintervals.append(x)
				cur_dur += maxtime

	words = IntervalTier(name='words')
	for i in wordintervals:
		words.addInterval(i)
	phones = IntervalTier(name='phones')
	for i in phoneintervals:
		phones.addInterval(i)
	tg1 = TextGrid(maxTime = cur_dur)
	tg1.append(words)
	tg1.append(phones)
	tg1.write(chapteroutpath1, null = '')

	speaker_tier = IntervalTier(name=speaker)
	for i in range(len(groupedwavfiles)):
		if i == 1:
			speaker_tier.add(0.0, wavfiletimes[0], groupedlabtext[0])
		else:
			speaker_tier.add(wavfiletimes[i-2], wavfiletimes[i-1], groupedlabtext[i-1])
	tg2 = TextGrid(maxTime = duration)
	tg2.append(speaker_tier)
	tg2.write(chapteroutpath2, null = '')



