import json

def main():
    with open('ids.json') as f:
        mons = json.load(f)
    names = {}
    for id, value in mons.items():
        names[value['name']] = id
    with open('parsed/names.json', 'w') as f:
        json.dump(names, f)
    return
main()