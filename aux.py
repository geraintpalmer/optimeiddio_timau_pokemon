import random
types = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

class Pokemon:
    def __init__(self, i, pdata, mdata, learnset, symudiadau=None):
        self.i = i
        row = pdata.loc[i]
        symudiadau_posib = list(learnset.loc[i][learnset.loc[i] == 1].index)
        self.enw = row['Name']
        self.types = [row['Type1'], row['Type2']]
        self.hp = int((2 * row['HP'] * 50) / 100) + row['HP'] + 50
        self.attack = int((2 * row['Attack'] * 50) / 100 + 5)
        self.spattack = int((2 * row['SpAttack'] * 50) / 100 + 5)
        self.defense = int((2 * row['Defense'] * 50) / 100 + 5)
        self.spdefense = int((2 * row['SpDefense'] * 50) / 100 + 5)
        self.speed = int((2 * row['Speed'] * 50) / 100 + 5)
        self.effeithiau = {t: row[t] for t in types}
        if symudiadau:
            self.symudiadau = [mdata.loc[int(a)] for a in symudiadau]
        else:
            self.symudiadau = [mdata.loc[int(a)] for a in random.sample(symudiadau_posib, 4)]
        self.iechyd = self.hp
    
    def adnewyddu(self):
        self.iechyd = self.hp
    
    def __repr__(self):
        return self.enw
    
    def cyfrifo_niwed(self, symudiad, gelyn):
        stab = 1 + (int(symudiad['Type'] in self.types) / 2)
        if symudiad['Class'] == 'Physical':
            mul = self.attack / gelyn.defense
        if symudiad['Class'] == 'Special':
            mul = self.spattack / gelyn.spdefense
        niwed = int((((22 * symudiad['Power'] * mul) / 50) + 2) * stab * gelyn.effeithiau[symudiad['Type']])
        return niwed

    def dewis_symudiad(self, gelyn):
        niwed_posib = [self.cyfrifo_niwed(a, gelyn) for a in self.symudiadau]
        dewis = max((x, i) for i, x in enumerate(niwed_posib))[1]
        return self.symudiadau[dewis]
    
    def ymosod(self, gelyn, symudiad):
        rnd = random.random() * 100
        if rnd < symudiad['Accuracy']:
            rand = random.randint(85, 100)
            niwed = int(self.cyfrifo_niwed(symudiad, gelyn) * (rand / 100))
        else:
            niwed = 0
        gelyn.iechyd = max(gelyn.iechyd - niwed, 0)


class Brwydr:
    def __init__(self, team1, team2):
        self.tim = team1
        self.tim_gelyn = team2
        for pkmn1, pkmn2 in zip(self.tim, self.tim_gelyn):
            pkmn1.adnewyddu()
            pkmn2.adnewyddu()
        self.pkmn_presennol_fi = random.choice([0, 1, 2, 3, 4, 5])
        self.pokemon_presennol_gelyn = random.choice([0, 1, 2, 3, 4, 5])
        self.buddugoliaethau_fi = 0
        self.buddugoliaethau_gelyn = 0
    
    def rhedeg(self):
        tro = 0
        while self.buddugoliaethau_fi != 6 and self.buddugoliaethau_gelyn != 6 and tro < 3000:
            fi = self.tim[self.pkmn_presennol_fi]
            gelyn = self.tim_gelyn[self.pokemon_presennol_gelyn]
            if fi.speed < gelyn.speed:
                cyntaf = fi
                ail = gelyn
            elif gelyn.speed < fi.speed:
                cyntaf = gelyn
                ail = fi
            else:
                ni = [fi, gelyn]
                random.shuffle(ni)
                cyntaf, ail = ni
            symudiad_1af = cyntaf.dewis_symudiad(ail)
            symudiad_2il = ail.dewis_symudiad(cyntaf)
            cyntaf.ymosod(ail, symudiad_1af)
            if ail.iechyd != 0:
                ail.ymosod(cyntaf, symudiad_2il)
            
            if fi.iechyd == 0:
                self.buddugoliaethau_gelyn += 1
                if self.buddugoliaethau_gelyn != 6:
                    self.pkmn_presennol_fi = random.choice([i for i, pkmn in enumerate(self.tim) if pkmn.iechyd != 0])
            if gelyn.iechyd == 0:
                self.buddugoliaethau_fi += 1
                if self.buddugoliaethau_fi != 6:
                    self.pokemon_presennol_gelyn = random.choice([i for i, pkmn in enumerate(self.tim_gelyn) if pkmn.iechyd != 0])
            tro += 1
        return self.buddugoliaethau_fi == 6


def creu_hap_tim(pdata, mdata, learnset):
    return [Pokemon(i, pdata, mdata, learnset) for i in random.sample(list(pdata.index), 6)]