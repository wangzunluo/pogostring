import json

REXT = '.csv'
PEXT = '.json'
PVE = 'pve'
RPATH = 'raw/'
PVPM = 'cp10000_all_overall_rankings'
PVPG = 'cp1500_all_overall_rankings'
PVPU = 'cp2500_all_overall_rankings'
PPATH = 'parsed/'

def parse_types(line, parsed):
    types = line.split('","')
    types = [i.split(' ')[0] for i in types if ' ' in i]
    for t in types:
        parsed[t] = []
    return types

def parse_labels(line):
    values = line.split('","')
    return [values[1].split(' ')[1]] + values[2:12]

def parse_pve():
    f = open(RPATH + PVE + REXT, 'r')
    raw = f.readlines()
    f.close()
    parsed = {}
    t_order = parse_types(raw[0][:-1], parsed)
    labels = parse_labels(raw[0])
    for line in range(1,23):
        items = raw[line][:-5].split('","')
        count_t = 0
        count_label = 0
        skip_count = 0
        pkmn = {}
        for i in items[1:]:
            if skip_count != 0:
                skip_count -= 1
                continue
            if i == '':
                if count_label == 0:
                    skip_count = 11
                    count_t += 1
                    continue
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
    parse_poke(PVPM)

def ultra():
    parse_poke(PVPU)

def great():
    parse_poke(PVPG)

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

main()