import json

def main():
    with open('evo.json') as f:
        mons = json.load(f)
    devo = {}
    for mon in mons:
        for evo in mon['evolutions']:
            devo[evo['pokemon_name']] = mon['pokemon_name']
    with open('parsed/devo.json', 'w') as f:
        json.dump(devo, f)
    return
main()