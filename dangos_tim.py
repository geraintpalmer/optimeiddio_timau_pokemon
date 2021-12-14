"""
Usage: gwerthuso.py <enw-tim>

Arguments
    enw-tim     : Enw'r ffeil lle mae data y tim wedi'i storio
Options
    -h          : displays this help file
"""
import docopt
import pandas as pd
import csv

arguments = docopt.docopt(__doc__)
enw_tim = arguments['<enw-tim>']

pdata = pd.read_csv('data/pdata_base.csv', index_col=0)
mdata = pd.read_csv('data/allowed_moves.csv', index_col=0)
learnset = pd.read_csv('data/learnset_base.csv', index_col=0)

tim_index = []
symudiadau_tim = []
with open('timau/' + enw_tim, 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        tim_index.append(int(row[0]))
        symudiadau_tim.append([int(r) for r in row[1:]])

tim = [pdata.loc[p]['Name'] for p in tim_index]
symudiadau = [[mdata.loc[a]['Name'] for a in symudiadau_tim[p]] for p in range(6)]

for i, p in enumerate(tim):
	print(p)
	print(f'        {symudiadau[i][0]}')
	print(f'        {symudiadau[i][1]}')
	print(f'        {symudiadau[i][2]}')
	print(f'        {symudiadau[i][3]}')