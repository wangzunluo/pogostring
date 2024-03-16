import json
import parse

PRE = [
    'Shadow ',
    'Mega ',
    'Apex ',
    'A ',
    'Primal ',
    'Galarian',
]

SUF = [

]

allpkmn = set()

def filter_name(name):
    if 'Tapu' in name:
        return name

    if ' ' in name:
        pkmn_index = 1
        if '(' in name:
            pkmn_index = 0
        elif ' - ' in name:
            pkmn_index = 0
        elif ' A ' in name:
            pkmn_index = 2
        elif ' Alolan ' in name:
            pkmn_index = 2
        if name.split(' ')[pkmn_index] == 'Shadow':
            pkmn_index = 1
        return name.split(' ')[pkmn_index]
    
    return name

def filterpvp():
    global allpkmn
    pvps = [
        parse.PPATH + parse.PVPG + parse.PEXT,
        parse.PPATH + parse.PVPU + parse.PEXT,
        parse.PPATH + parse.PVPM + parse.PEXT
    ]
    pvpmons = []
    for pvp in pvps:
        with open(pvp) as f:
            pvpmons.append(json.load(f))
    
    for league in pvpmons[0:2]:
        for pkmn in list(league.keys())[:200]:
            allpkmn.add(filter_name(pkmn))
    
    for pkmn in list(pvpmons[2].keys())[:100]:
        allpkmn.add(filter_name(pkmn))
    return

def main():
    pve = None
    global allpkmn
    with open(parse.PPATH + parse.PVE + parse.PEXT) as f:
        pve = json.load(f)
    for ptype, plist in pve.items():
        for pkmn in plist:
            allpkmn.add(filter_name(pkmn['Pokemon']))

def add_modifiers(pkmnset):
    pkmnset.add('shadow')
    pkmnset.add('4*')
    pkmnset.add('shiny')
    pkmnset.add('legendary')
    pkmnset.add('mythical')

def shorten():
    printme = set()
    with open('parsed/devo.json') as f:
        devo = json.load(f)

    with open('parsed/names.json') as f:
        names = json.load(f)

    for mon in allpkmn:
        printme.add(names.get(mon, mon))
        devomon = devo.get(mon)
        while devomon:
            printme.add(names[devomon])
            devomon = devo.get(devomon)
    add_modifiers(printme)
    print(*printme, sep ='& !')

main()
filterpvp()
shorten()