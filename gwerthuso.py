"""
Usage: gwerthuso.py <enwffeil>

Arguments
    enwffeil   : enw'r ffeil i werthuso
Options
    -h          : displays this help file
"""
import docopt
import pandas as pd
import tqdm
import csv
import random
import aux

arguments = docopt.docopt(__doc__)
enwffeil = str(arguments['<enwffeil>'])

pdata = pd.read_csv('data/pdata_base.csv', index_col=0)
mdata = pd.read_csv('data/allowed_moves.csv', index_col=0)
learnset = pd.read_csv('data/learnset_base.csv', index_col=0)

tim_index = []
symudiadau_tim = []
with open('timau/' + enwffeil, 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        tim_index.append(int(row[0]))
        symudiadau_tim.append([int(r) for r in row[1:]])


tim_gorau = [aux.Pokemon(i, pdata, mdata, learnset, symudadau) for i, symudadau in zip(tim_index, symudiadau_tim)]
print([t.enw for t in tim_gorau])

canlyniadau = []
random.seed(1)
for treial in tqdm.tqdm(range(1000)):
	hapdim = aux.creu_hap_tim(pdata, mdata, learnset)
	for _ in range(10):
		B = aux.Brwydr(tim_gorau, hapdim)
		canlyniadau.append(B.rhedeg())

c = sum(canlyniadau) / len(canlyniadau)
with open('canlyniadau/' + enwffeil, 'w') as f:
	f.write(str(c))
