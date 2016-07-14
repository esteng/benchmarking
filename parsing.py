import os
import shutil
import subprocess

#directory = r'D:\Data\LibriSpeech\test-clean'
#out_directory = r'D:\Data\LibriSpeech\standard'

directory = 'LibriSpeech/dev-clean'
out_directory = 'LibriSpeech/standard'


speakers = os.listdir(directory)

utt_trans_mapping = {}
utt_file_mapping = {}
speak_utt_mapping = {}

for s in speakers:
    speak_dir = os.path.join(directory, s)
    discourses = os.listdir(speak_dir)
    speak_utt_mapping[s] = []
    for d in discourses:
        discourse_dir = os.path.join(speak_dir, d)
        trans_file = os.path.join(discourse_dir, '{}-{}.trans.txt'.format(s, d))
        with open(trans_file, 'r') as f:
            for line in f:
                line = line.strip()
                utt, line = line.split(maxsplit=1)
                utt_trans_mapping[utt] = line
                utt_file_mapping[utt] = os.path.join(discourse_dir, '{}.flac'.format(utt))
                speak_utt_mapping[s].append(utt)

for s, utts in speak_utt_mapping.items():
    speak_dir = os.path.join(out_directory, s)
    os.makedirs(speak_dir, exist_ok = True)
    for u in utts:
        lab_path = os.path.join(speak_dir, '{}.lab'.format(u))
        flac_path = os.path.join(speak_dir, '{}.wav'.format(u))
        with open(lab_path, 'w', encoding = 'utf8') as f:
            f.write(utt_trans_mapping[u])
        subprocess.call(['sox', utt_file_mapping[u].replace('\\','/'), flac_path.replace('\\','/')])
#        shutil.copy(utt_file_mapping[u], flac_path)
