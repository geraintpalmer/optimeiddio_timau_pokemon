"""
Usage: optimeiddio.py <cymhareb> <ychwanegol>

Arguments
    cymhareb   : Cymhareb y pwysau ar gyfer f1 ac f2
    ychwanegol : 1 os oes angen y cyfyngiad ychwanegol, 0 fel arall
Options
    -h          : displays this help file
"""
import docopt
import pandas as pd
import pulp
import csv

arguments = docopt.docopt(__doc__)
cymhareb = float(arguments['<cymhareb>'])
ychwanegol = float(arguments['<ychwanegol>'])

# Paratoi'r data
def cyfanswm_stats(row):
    if row['Special Attacker']:
        return row['HP'] + row['SpAttack'] + row['Defense'] + row['SpDefense'] + row['Speed']
    return row['HP'] + row['Attack'] + row['Defense'] + row['SpDefense'] + row['Speed']

matrics_effeithiau = [
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1,],
    [1, 0.5, 2, 1, 0.5, 0.5, 1, 1, 2, 1, 1, 0.5, 2, 1, 1, 1, 0.5, 0.5,],
    [1, 0.5, 0.5, 2, 2, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1,],
    [1, 1, 1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 1,],
    [1, 2, 0.5, 0.5, 0.5, 2, 1, 2, 0.5, 2, 1, 2, 1, 1, 1, 1, 1, 1,],
    [1, 2, 1, 1, 1, 0.5, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1,],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 0.5, 1, 1, 0.5, 1, 2,],
    [1, 1, 1, 1, 0.5, 1, 0.5, 0.5, 2, 1, 2, 0.5, 1, 1, 1, 1, 1, 0.5,],
    [1, 1, 2, 0, 2, 2, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1,],
    [1, 1, 1, 2, 0.5, 2, 0.5, 1, 0, 1, 1, 0.5, 2, 1, 1, 1, 1, 1,],
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 0.5, 2, 1, 2, 1, 2, 1, 1,],
    [1, 2, 1, 1, 0.5, 1, 0.5, 1, 0.5, 2, 1, 1, 2, 1, 1, 1, 1, 1,],
    [0.5, 0.5, 2, 1, 2, 1, 2, 0.5, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 1,],
    [0, 1, 1, 1, 1, 1, 0, 0.5, 1, 1, 1, 0.5, 1, 2, 1, 2, 1, 1,],
    [1, 0.5, 0.5, 0.5, 0.5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2,],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 2, 1, 0.5, 1, 0.5, 1, 2,],
    [0.5, 2, 1, 1, 0.5, 0.5, 2, 0, 2, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 1, 0.5, 0.5,],
    [1, 1, 1, 1, 1, 1, 0.5, 2, 1, 1, 1, 0.5, 1, 1, 0, 0.5, 2, 1]
]

pdata = pd.read_csv('data/pdata_base.csv', index_col=0)
mdata = pd.read_csv('data/allowed_moves.csv', index_col=0)
learnset = pd.read_csv('data/learnset_base.csv', index_col=0)

mdata = mdata.loc[[int(i) for i in learnset.columns]]

pdata['Special Attacker'] = (pdata['SpAttack'] >= pdata['Attack']).astype(int)
pdata['Physical Attacker'] = (pdata['Attack'] >= pdata['SpAttack']).astype(int)
pdata['TotalStats'] = pdata.apply(cyfanswm_stats, axis=1)
mdata['Special'] = (mdata['Class'] == 'Special').astype('int')
mdata['Physical'] = (mdata['Class'] == 'Physical').astype('int')
types = list(pdata.columns[-21:-3])

resistances = {p: {t: int(pdata.loc[p, t] < 1) for t in types} for p in pdata.index}
weaknesses = {p: {t: int(pdata.loc[p, t] > 1) for t in types} for p in pdata.index}
strong_against = {a: {t: int(matrics_effeithiau[types.index(t)][types.index(mdata.loc[a]['Type'])] > 1) for t in types} for a in mdata.index}
stab = {p: {a: int(mdata.loc[a, 'Type'] in [pdata.loc[p, 'Type1'], pdata.loc[p, 'Type2']]) for a in mdata.index} for p in pdata.index}

if ychwanegol == 1:
    G = {t: {m: int(mdata.loc[m, 'Type'] == t) for m in mdata.index} for t in types}

indexes = []
pmoves = {}
for p in pdata.index:
    pmoves[p] = [int(a) for a in learnset.loc[p][learnset.loc[p]==1].index]
    indexes += [(p, int(a)) for a in learnset.loc[p][learnset.loc[p]==1].index]

Gamma = 0

if ychwanegol == 1:
    with open('params/max_f1_ych.csv', 'r') as f:
        maxf1 = float(f.read())
    with open('params/max_f2_ych.csv', 'r') as f:
        maxf2 = float(f.read())
else:
    with open('params/max_f1.csv', 'r') as f:
        maxf1 = float(f.read())
    with open('params/max_f2.csv', 'r') as f:
        maxf2 = float(f.read())

# Datrys

prob = pulp.LpProblem("TimPokemonGorau", pulp.LpMaximize)
X = pulp.LpVariable.dicts("X", pdata.index, cat=pulp.LpBinary)
Y = pulp.LpVariable.dicts("Y", indexes, cat=pulp.LpBinary)

f1 = (sum(X[p] * pdata.loc[p, 'TotalStats'] for p in pdata.index))
f2 = sum((1 + (0.5 * stab[p][a])) * mdata.loc[a, 'Power'] * mdata.loc[a, 'Accuracy'] * Y[(p, a)] for p in pdata.index for a in pmoves[p])

objective_function = (cymhareb * (f1 / maxf1)) +  ((1 - cymhareb) * (f2 / maxf2)) # Defnyddio unwaith my maxf1 a maxf2 gyda chi
# objective_function = (cymhareb * f1) +  ((1 - cymhareb) * f2) # Defnyddio i canfod maxf1 a maxf2
prob += objective_function

prob += sum(X[p] for p in pdata.index) == 6
prob += sum(Y[(p, a)] for p in pdata.index for a in pmoves[p]) == 24
prob += sum(X[p] * pdata.loc[p]['Special Attacker'] for p in pdata.index) >= 2
prob += sum(X[p] * pdata.loc[p]['Physical Attacker'] for p in pdata.index) >= 2
for p in pdata.index:
    prob += sum(Y[(p, a)] for a in pmoves[p]) == (4 * X[p])
    prob += sum(Y[(p, a)] * (1 - pdata.loc[p, 'Special Attacker']) * mdata.loc[a, 'Special'] for a in pmoves[p]) <= Gamma
    prob += sum(Y[(p, a)] * (1 - pdata.loc[p, 'Physical Attacker']) * mdata.loc[a, 'Physical'] for a in pmoves[p]) <= Gamma
for t in types:
    prob += sum(Y[(p, a)] * (1 - weaknesses[p][t]) * strong_against[a][t] for p in pdata.index for a in pmoves[p]) >= 1
    prob += sum(X[p] * resistances[p][t] for p in pdata.index) >= 1
    if ychwanegol == 1:
        for p in pdata.index:
            prob += sum(Y[p, a] * G[t][a] for a in pmoves[p]) <= 1


prob.solve()

# print(prob.objective.value()) # Er mwyn cael maxf1 a maxf2


team = []
moves = []
for p in pdata.index:
    if X[p].value() == 1:
        team.append(p)
        mon = pdata.loc[p, 'Name']
        chosen_moves = [a for a in pmoves[p] if Y[(p, a)].value() == 1]
        moves.append(chosen_moves)

if ychwanegol == 1:
    filename = f'timau/tim_ychwanegol_={round(cymhareb, 6)}.csv'
else:
    filename = f'timau/tim_={round(cymhareb, 6)}.csv'

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for p in range(6):
        row = [team[p]] + moves[p]
        csvwriter.writerow(row)
