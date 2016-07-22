# benchmarking
Bencharking suites for PolyglotDB

In the MFA folder, there are several scripts beginning with benchmark\_aligner, one per dataset. There are currently scripts to align the LibriSpeech corpus and the lab datasets for Quebec French, English, and Tagalog. If dict\_path = None, the --nodict option is implemented (as in the Tagalog script). The paths to the relevant directories, as well as the number of jobs, can be changed at the top of the scripts. The models from alignment are stored in zip folders.

The reorganize\_french\_corpus.py script restructures the Quebec French dataset into a usable format for alignment.

The comparetextgrids.py script takes two paths to aligned corpora as command line arguments and outputs a csv file showing the average differences in word, phone, and segment-of-interest alignment, as well as the difference in counts of 'sil' segments. If a textgrid in one dataset does not have a corresponding one in the other dataset, nothing is outputted. If segments of interest are not indicated in a textgrid, there will be a blank space in the SOI column of the csv. In cases where the two alignments have different phone counts, the two counts will be listed and no average difference will be given.
