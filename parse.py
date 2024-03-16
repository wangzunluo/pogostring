import json

REXT = '.csv'
PEXT = '.json'
PVE = 'pve'
RPATH = 'raw/'
PVPM = 'pvpm'
PVPG = 'pvpg'
PVPU = 'pvpu'
PPATH = 'parsed/'

def parse_types(line, parsed):
    types = line.split(',')
    types = [i for i in types if i != '']
    for t in types:
        parsed[t] = []
    return types

def parse_labels(line):
    return line.split(',')[1:12]

def parse_pve():
    f = open(RPATH + PVE + REXT, 'r')
    raw = f.readlines()
    f.close()
    parsed = {}
    t_order = parse_types(raw[1][:-1], parsed)
    labels = parse_labels(raw[2])
    for line in range(3,25):
        items = raw[line][:-1].split(',')
        count_t = 0
        count_label = 0
        pkmn = {}
        for i in items[1:]:
            if i == '':
                parsed[t_order[count_t]] += [pkmn]
                pkmn = {}
                count_label = 0
                count_t += 1
                continue
            pkmn[labels[count_label]] = i
            count_label += 1
        parsed[t_order[count_t]] += [pkmn]
            
    f = open(PPATH + PVE + PEXT, 'w')
    json.dump(parsed, f)
    f.close()

def parse_generic(filename):
    f = open(RPATH + filename + REXT, 'r')
    raw = f.readlines()
    f.close()
    parsed = []
    labels = raw[5][:-1].split(',')[1:]
    labels[3] = 'Type1'
    labels[4] = 'Type2'
    labels[6] = 'Count1'
    labels[8] = 'Count2'
    pkmn = {}
    for line in range(6,56):
        items = raw[line][:-1].split(',', 10)
        pkmn = {}
        for index, i in enumerate(items[1:]):
            pkmn[labels[index]] = i
        pkmn[labels[-1]] = pkmn[labels[-1]][1:-1]
        parsed += [pkmn]
    f = open(PPATH + filename + PEXT, 'w')
    json.dump(parsed, f)
    f.close()

def master():
    parse_generic(PVPM)

def ultra():
    parse_generic(PVPU)

def great():
    parse_generic(PVPG)

def parse_pvp():
    master()
    ultra()
    great()

def parse_poke(filename):
    with open(RPATH + filename + REXT, 'r') as f:
        raw = f.readlines()
    labels = raw[0][:-1].split(',')
    alldata = {}
    for line in raw[1:]:
        pkmn = {}
        pkmndata = line[:-1].split(',')
        for index, data in enumerate(pkmndata):
            pkmn[labels[index]] = data
        alldata[pkmndata[0]] = pkmn
    with open(PPATH + filename + PEXT, 'w') as f:
        json.dump(alldata, f)

def main():
    parse_pve()
    parse_pvp()

# main()
parse_poke('cp1500_all_overall_rankings')