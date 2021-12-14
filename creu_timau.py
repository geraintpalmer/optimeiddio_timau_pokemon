"""
Usage: creu_timau.py <nifer>

Arguments
    nifer  : Nifer o dimau i greu
Options
    -h          : displays this help file
"""
import docopt
import random
import aux
import pandas as pd
import csv

arguments = docopt.docopt(__doc__)
n = int(arguments['<nifer>'])

pdata = pd.read_csv('data/pdata_base.csv', index_col=0)
mdata = pd.read_csv('data/allowed_moves.csv', index_col=0)
learnset = pd.read_csv('data/learnset_base.csv', index_col=0)

random.seed(0)
for i in range(n):
    tim = aux.creu_hap_tim(pdata, mdata, learnset)
    tim_index = [p.i for p in tim]
    symudiadau_tim = [[m.name for m in p.symudiadau] for p in tim]
    with open(f'timau/haptim_{i}.csv', 'w', newline='') as csvfile:
    	csvwriter = csv.writer(csvfile, delimiter=',')
    	for p in range(6):
        	row = [tim_index[p]] + symudiadau_tim[p]
        	csvwriter.writerow(row)
