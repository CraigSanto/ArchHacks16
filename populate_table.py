import rethinkdb as r
import random
import json
import time
from get_county_coords import get_lat_lon

def get_random_name():
    first_names = open('first_names.txt').read().splitlines()
    last_names = open('last_names.txt').read().splitlines()
    f_line = random.choice(first_names)
    l_line = random.choice(last_names)
    return (f_line + " " + l_line)

def get_random_county():
    counties = open('counties.txt').read().splitlines()
    return (random.choice(counties))

def get_random_pref():
    pref = ['allergies','vision',
            'childcare', 'general',
            'mental', 'illness', 'nutritional',
            'sexual health', 'pregnant', 'physical']
    ret_pref = []
    for i in range(random.randint(1, len(pref)/2)):
        t = random.choice(pref)
        if t not in ret_pref:
            ret_pref.insert(0,t)
#        else:
#            i=-1;
    return ret_pref






host = "DESKTOP-K4G0PLO"
db_name = 'ArchHacks'
table_name = 'People'
r.connect(host=host).repl()
r.db(db_name).table(table_name).delete().run()
co = get_lat_lon()
ids = []
while True:
    name = get_random_name()
    county = get_random_county()
    pref = get_random_pref()
    take = random.randint(1, 100000)
    while take in ids:
        take = random.randint(1, 100000)
    ids.append(take)


    r.db(db_name).table(table_name).insert([
    {"name": name,
    "id": take,
    "location": county,
    "coordinates": co[county],
    "preferences":pref,
     "status": False}
    ]).run()

    #print(name +" of " + county + " who needs " + str(pref))
    r.db(db_name).table(table_name).filter({'status':True}).delete().run()
#cursor = r.db(db_name).table(table_name).run()
#for d in cursor:
#    print(d['name'])
