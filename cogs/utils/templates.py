import json

with open('catalogue.json', 'r') as f:
    catalogue = json.load(f)


atlas = catalogue['Ships'][1]['Atlas']
statan = catalogue['Planets'][1]['Statan']


NEW_ACC = {
    "balance": 0,
    "inventory": {},
    "ships": {"Atlas":atlas},
    "planets": {"Statan":statan},
    "pets": []
}
