# -*- coding: utf-8 -*-
sys.path.append('c:/aloumiotis/python/lib')
import os, copy, cPickle
from datetime import datetime
import pprint as pp
import my_util_new as my
import cPickle, os, csv, pprint
from datetime import datetime
from datetime import date
os.chdir('r:/wd/riad')
pp = pp.pprint

x = date(9999,12,31)
rdate = datetime.strptime('2015/12/24', '%Y/%m/%d') 
rdate = rdate.date() 
print rdate
print x
riad = {}
with open('riadDwhS123_4.csv') as csvfile:
    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        riad[row['riadid'][2:]] = {'sector': row['sector'].replace('.', ''), 
            'subsector': row['subsector'].replace('.','')}                        

mapping = my.riadMap()
for key, val in mapping.iteritems():
    if val[0] in riad.keys(): 
        riad[val[0]].update({'bogid':key, 'bogmid':int(val[1]), 'riadmid':val[2],
            'grname':val[4].decode('utf8')}) 

mapping = my.riadNew()
for key, val in mapping.iteritems():
    if val[0] in riad.keys(): riad[val[0]].update({'bogid':key, 'bogmid':int(val[1]), 'riadmid':val[2],
            'grname':val[4]}) 

mapping = my.riadOther()
for key, val in mapping.iteritems():
    if val[0] in riad.keys(): riad[val[0]].update({'bogid':key, 'bogmid':key, 'riadmid':val[0]}) 

addresses = {}
with open('addresses.txt') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ';', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        addresses[row['riad_mgmt_code']] = {'name': row['name'], 'address': row['address'],
            'city': row['city'], 'zipcode': row['zipcode']}                        

with open('riadAddresses.csv') as csvfile:
    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row['riadid'][2:] in addresses.keys():
            addresses[row['riadid'][2:]] = {'name': row['name'], 'address': row['address'],
            'city': row['city'], 'zipcode': row['zipcode']}

riadPickle = {'mapping':riad, 'address':addresses}
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riadPickle, output)

with open('riadAddresses.csv') as csvfile:
    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row['riadid'][2:] in addresses.keys():
            addresses[row['riadid'][2:]] = {'name': row['name'], 'address': row['address'],
            'city': row['city'], 'zipcode': row['zipcode']}

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
print riad.keys()

keys = [7001, 7002, 8001, 8002, 8003, 8004, 8005]
for k in keys:
    l = riad['mapping']['IVF{}'.format(k)]
    l['bogid'] = k 

keys = [3005]
for k in keys:
    l = riad['mapping']['IVF{}'.format(k)]
    l['bogid'] = 475 

riad['bogmapping'] = {}
for k, v in riad['mapping'].items():
    try: riad['bogmapping'][int(v['bogid'])] 
    except:
        riad['bogmapping'][int(v['bogid'])] = k
    else:
        print riad['bogmapping'][int(v['bogid'])]

with open('riadbackup.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

with open('names_births.csv') as f:
    csvReader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
    for row in csvReader:
        rdate = datetime.strptime(row['birthdate'], '%Y/%m/%d %H:%M:%S') 
        rdate = '{:%Y-%m-%d}'.format(rdate)
        riad['mapping'][row['id'][2:]]['birthdate'] = rdate 
        riad['mapping'][row['id'][2:]]['name'] = rdate 

with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

with open('names_births.csv') as f:
    csvReader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
    for row in csvReader:
        rdate = '9999-12-31'
        riad['mapping'][row['id'][2:]]['closedate'] = rdate 
riad['mapping']['IVF2003'] = {'birthdate':'2008-09-05'} 

with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

with open('names_births.csv') as f:
    csvReader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
    for row in csvReader:
        riad['mapping'][row['id'][2:]]['name'] = row['name'] 

with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
riad = riad['mapping']
keys = riad.keys()
pp.pprint(riad[keys[1]])
print riad.keys()
print riad['address']

with open('S126A_GR_names_births.csv') as f:
    csvReader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
    for row in csvReader:
        rdate = datetime.strptime(row['Birth Date'], '%Y/%m/%d %H:%M:%S') 
        rdate = '{:%Y-%m-%d}'.format(rdate)
        riad['mapping'][row['RIAD Code'][2:]] = {'name':row['Orgunit Name'], 'bogid':row['RIAD Code'][2:], 'bogmid':row['RIAD Code'][2:], 'closedate':'9999-12-31', 'riadmid':row['RIAD Code'][2:], 'sector':'S126', 'subsector':'S126A', 'birthdate':rdate}
        riad['bogmapping'][row['RIAD Code'][2:]] = row['RIAD Code'][2:]

# -*- coding: utf-8 -*-
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
    end = date(9999,12,31)
    now = datetime.now()
for k, v in riad['mapping'].items():
    birth = v['birthdate'] 
    if 'sector' not in v.keys(): sector = ''
    else: 
        sector = v['sector']
    if 'subsector' not in v.keys(): subsector = ''
    else: 
        subsector = v['subsector']
    riad['mapping'][k]['sector'] = [[sector, birth, end, now]]
    riad['mapping'][k]['subsector'] = [[subsector, birth, end, now]]
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)
print riad.keys()
del riad['closedate']
end = date(9999,12,31)
for k, v in riad['mapping'].items():
    birth = datetime.strptime(v['birthdate'], '%Y-%m-%d').date() 
    riad['mapping'][k]['birthdate'] = birth
    riad['mapping'][k]['closedate'] = end
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riadX = cPickle.load(f) 
riadX['mapping'] = riad
for k, v in riadX['mapping'].items():
    riadX['mapping'][k]['MANAGEDBY'] = riadX['mapping'][k].pop('riadmid')
    riadX['mapping'][k]['CLOSEDATE'] = riadX['mapping'][k].pop('closedate')
    riad['mapping'][k]['RIAD_NAME'] = riad['mapping'][k].pop('name')
    riad['mapping'][k]['RIAD_SECTOR'] = riad['mapping'][k].pop('sector')
    old = riad['mapping'][k]['RIAD_SECTOR']  
    oldss = riad['mapping'][k]['subsector'] 
    riad['mapping'][k]['RIAD_SECTOR'] = [[old[0][0], oldss[0][0], old[0][1], old[0][2], old[0][3]]]  
    del riad['mapping'][k]['subsector'] 
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)
print riad.keys()
del riad['closedate']
end = date(9999,12,31)
for k, v in riad['mapping'].items():
    birth = datetime.strptime(v['birthdate'], '%Y-%m-%d').date() 
    riad['mapping'][k]['birthdate'] = birth
    riad['mapping'][k]['closedate'] = end

with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)
with open('riadbackup.pkl', 'wb') as output:
    cPickle.dump(riad, output)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['mapping'] 
for k in r.keys():
    try:
        kma = r[k]['RIAD_ISMANAGEMENTOF']
    except:
        continue
    else:
        for k1 in kma.keys():
            print kma[k1][0]
            kma[k1] = kma[k1][0]

keys = r.keys()
pp.pprint(r)

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
print riad.keys()
r = riad['mapping']
a = riad['address']
b = riad['bogmapping']
pp(r['1000'])
print r['1000']['RIAD_NAME'][0][1]
pp(a)
r = riad['mapping']
for k,v in renameDict.iteritems():
    r[v] = r.pop(k)
pp.pprint(r['MFMC008'])
pp.pprint(r['IVF2081'])
pp.pprint(r['IVF9011'])
pp.pprint(r['AEPEY1'])

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['mapping']
a = riad['address']
for k,v in renameDict.iteritems():
    r[v] = r.pop(k)
    a[v] = a.pop(k)

for k,v in renameDict.iteritems():
    b[v] = b.pop(k)
    b[v] = v

for k,v in renameDict.iteritems():
    r[v] = r.pop(k)
    a[v] = a.pop(k)

for k, v in r.iteritems():
    try:
        v['MANAGEDBY']
    except KeyError:
        continue
    else:
        for k1,v1 in renameDict.iteritems():
            try: 
                v['MANAGEDBY'][v1] = v['MANAGEDBY'].pop(k1)
            except KeyError:
                continue


with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['mapping']
a = riad['address']
renameDict = dict(AUX5001='MFMC1',
                AUX5002='MFMC2',
                AUX5003='MFMC3',
                AUX5004='MFMC4',
                AUX5006='MFMC8',
                AUX5007='MFMC9',
                AUX5008='MFMC10',
                AUX5010='MFMC12',
                AUX5011='MFMC13',
                AUX5012='MFMC14',
                AUX5013='MFMC15',
                AUX5014='MFMC16',
                AUX5016='MFMC18',
                AUX5019='MFMC22')

for k, v in r.items():
    try:
        x = r[k]['MANAGEDBY']
    except KeyError:
        continue
    else:
        for mk in x.keys():
            x[mk] = x[mk][1:] 

pp.pprint(r[r.keys()[2]])
    riad['mapping'][k]['MANAGEDBY'] =  
    riadX['mapping'][k]['CLOSEDATE'] = riadX['mapping'][k].pop('closedate')
    riad['mapping'][k]['RIAD_NAME'] = riad['mapping'][k].pop('name')
    riad['mapping'][k]['RIAD_SECTOR'] = riad['mapping'][k].pop('sector')

riadX['mapping'] = riad
for k, v in riadX['mapping'].items():
    riadX['mapping'][k]['MANAGEDBY'] = riadX['mapping'][k].pop('riadmid')
    riadX['mapping'][k]['CLOSEDATE'] = riadX['mapping'][k].pop('closedate')
    riad['mapping'][k]['RIAD_NAME'] = riad['mapping'][k].pop('name')
    riad['mapping'][k]['RIAD_SECTOR'] = riad['mapping'][k].pop('sector')
    old = riad['mapping'][k]['RIAD_SECTOR']  
    oldss = riad['mapping'][k]['subsector'] 
    riad['mapping'][k]['RIAD_SECTOR'] = [[old[0][0], oldss[0][0], old[0][1], old[0][2], old[0][3]]]  
    del riad['mapping'][k]['subsector'] 

os.chdir('r:/wd/riad')
os.chdir('M:/process/pickles/backup')
os.chdir('M:/process/pickles')

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['mapping']
a = riad['address']
b = riad['bogmapping']

renameDict = dict(AUX5001='MFMC1',
                AUX5002='MFMC2',
                AUX5003='MFMC3',
                AUX5004='MFMC4',
                AUX5005='MFMC5',
                AUX5006='MFMC8',
                AUX5007='MFMC9',
                AUX5008='MFMC10',
                AUX5010='MFMC12',
                AUX5011='MFMC13',
                AUX5012='MFMC14',
                AUX5013='MFMC15',
                AUX5014='MFMC16',
                AUX5016='MFMC18',
                AUX5018='MFMC20',
                AUX5019='MFMC22',
                FCL0001='LEA1',
                FCL0002='LEA2',
                FCL0003='LEA7',
                FCL0004='LEA8',
                FCL0005='LEA9',
                FCL0006='LEA10',
                FCL0007='LEA11',
                FCL0008='LEA12',
                FCL0009='LEA15',
                FCL0010='FAC101',
                FCL0011='FAC102',
                FCL0012='FAC103',
                FCL0013='FAC105',
                FCL0014='FAC106',
                FCL0015='CRE501',
                FCL0016='CRE502',
                FCL0017='CRE503',
                FCL0018='CRE504')


for k,v in renameDict.iteritems():
    r[v] = r.pop(k)
    try: a[k]
    except: pass
    else: a[v] = a.pop(k)
    b[v] = b.pop(k)
    b[v] = v

for k, v in r.iteritems():
    try:
        v['MANAGEDBY']
    except KeyError:
        continue
    else:
        for k1,v1 in renameDict.iteritems():
            try: 
                v['MANAGEDBY'][v1] = v['MANAGEDBY'].pop(k1)
            except KeyError:
                continue
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

os.chdir('M:/process/pickles')

with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['mapping']
a = riad['address']
b = riad['bogmapping']

for k in r['MFMC22']['RIAD_ISMANAGEMENTOF'].keys():
    r[k]['RIAD_NAME'][0][0] = r[k]['RIAD_NAME'][0][0].replace('Eurobank NTT', 'T.T. ELTA') 

with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['mapping']['GR']
a = riad['address']
b = riad['bogmapping']

for k in r.keys():
    r[k]['NOT_IN_RIAD'] = [False, False] 
    del r[k]['IS_IN_RIAD']

os.chdir('M:/process/pickles/backup')
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

r = riad['GR']
pp.pprint(r.keys())
pp.pprint(r['CRE501'])
pp.pprint(r['1071'])
pp.pprint(r['IVF2003'])
pp.pprint(r['IVF2061'])
pp.pprint(r['IVF2100'])
pp.pprint(b[807])
pp.pprint(r['AEPEY15'])
pp.pprint(r['IVF2081'])
pp.pprint(r[['IVF9011'])
pp.pprint(r['MFMC1'])
pp.pprint(r['MFMC10'])
pp.pprint(r['GR']['1056'])
pp.pprint(r['1073'])
a = riad['address']
pp.pprint(r['AEEAP2'])

# -*- coding: utf-8 -*-

test = 'τίτλος στα ελληνικά'.decode('utf8').encode('iso-8859-7')
os.chdir('M:/process/pickles')
with open('new_ivf.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ';', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['riadId','birthdate','closedate','countryofresidence','name','namegr','isin','lei','sector','subsector','address','city','postalcode','areacode','listed','supervised','licence','capital','ucits','legal','subfund','nace','mngt'])
    writer.writerow(['#IVF03186','2015-05-26','9999-31-12','GR','3K A/K GREEK VALUE DOMESTIC EQUITY',test,'[GRF00135001, GRF00136009]','','S.124','S.124.B','25-27-29 Karneadou Str','Athens','10675','U2','','T','GRF','OPEN_END','UCITS','U','','K64.30','MFMC14'])

import os, copy, cPickle
from datetime import datetime
import pprint as pp
os.chdir('M:/process/pickles/backup')
with open("riadFirst.pkl", "rb") as f:
    riad = cPickle.load(f) 
x = copy.deepcopy(riad['mapping'])
del riad['mapping']
riad['mapping'] = {}
riad['mapping']['GR'] = x 
r2= riad['mapping']['GR']
for k, v in r.iteritems():
    v['RIAD_ORGUNIT'] = [[r[k].pop('BIRTHDATE'), r[k].pop('CLOSEDATE'), 'GR', datetime(2015, 3, 30), 'aloumiotis']] 
    
for k, v in r.iteritems():
    r[k]['RIAD_AREACODE'] = [['U2', r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
    r[k]['RIAD_LICENSED'] = [['T', 'GRF', r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
    if v['RIAD_SECTOR'][0][1] == 'S126A':
        try: v['RIAD_ISMANAGEMENTOF']
        except KeyError: print 'no child companies of ' + k 
        else:
            for c in v['RIAD_ISMANAGEMENTOF'].iterkeys():
                r[c]['RIAD_ADDRESS'] = [[riad['address'][k]['address'], r[c]['RIAD_ORGUNIT'][0][0], r[c]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
                r[c]['RIAD_CITY'] = [[riad['address'][k]['city'], r[c]['RIAD_ORGUNIT'][0][0], r[c]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
                r[c]['RIAD_POSTALCODE'] = [[riad['address'][k]['zipcode'], r[c]['RIAD_ORGUNIT'][0][0], r[c]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
        try: riad['address'][k]
        except KeyError: print 'no address data for ' + k
        else:
            r[k]['RIAD_ADDRESS'] = [[riad['address'][k]['address'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
            r[k]['RIAD_CITY'] = [[riad['address'][k]['city'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
            r[k]['RIAD_POSTALCODE'] = [[riad['address'][k]['zipcode'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]

    if k in ['IVF7001', 'IVF7002', 'IVF8001', 'IVF8002', 'IVF8003', 'IVF8004', 'IVF8005']:
        try: riad['address'][k]
        except KeyError: print 'no address data for ' + k
        else:
            r[k]['RIAD_ADDRESS'] = [[riad['address'][k]['address'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
            r[k]['RIAD_CITY'] = [[riad['address'][k]['city'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
            r[k]['RIAD_POSTALCODE'] = [[riad['address'][k]['zipcode'], r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
    for sec in v['RIAD_SECTOR']:
        sec[4:7] = ['STAT', 'F', 'aloumiotis']
    for sec in v['RIAD_NAME']:
        sec[5:8] = ['STAT', 'F', 'aloumiotis']

for k, v in r.iteritems():
    if v['RIAD_SECTOR'][0][1] == 'S126A':
        try: v['RIAD_ISMANAGEMENTOF']
        except KeyError: print 'no child companies of ' + k 
        else:
            for c in v['RIAD_ISMANAGEMENTOF'].iterkeys():
                v['RIAD_ISMANAGEMENTOF'][c] = [v['RIAD_ISMANAGEMENTOF'][c] + ['STAT', 'F', 'aloumiotis']]
    try: v['MANAGEDBY']
    except KeyError: pass 
    else:
        for c in v['MANAGEDBY'].iterkeys():
            v['MANAGEDBY'][c] = [v['MANAGEDBY'][c] + ['STAT', 'F', 'aloumiotis']]

    if k in ['IVF7001', 'IVF7002', 'IVF8001', 'IVF8002', 'IVF8003', 'IVF8004', 'IVF8005']:
        r[k]['RIAD_CAPITALVARIABILITY'] = [['CLOSED', r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]
    elif k not in ['IVF7001', 'IVF7002', 'IVF8001', 'IVF8002', 'IVF8003', 'IVF8004', 'IVF8005'] and r[k]['RIAD_SECTOR'][0][0] in ['S124', 'S123']: 
        r[k]['RIAD_CAPITALVARIABILITY'] = [['OPEN_END', r[k]['RIAD_ORGUNIT'][0][0], r[k]['RIAD_ORGUNIT'][0][1], datetime(2015, 3, 30), 'STAT', 'F', 'aloumiotis']]

for k, v in r.iteritems():
    if k == 'IVF2003': continue
    x = v['RIAD_SECTOR'][0][0]   
    v['RIAD_SECTOR'][0][0] = x[0] + '.' + x[1:]
    x = v['RIAD_SECTOR'][0][1]   
    if len(x): v['RIAD_SECTOR'][0][1] = x[0] + '.' + x[1:-1] + '.' + x[-1]

os.chdir('M:/process/pickles')
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad['mapping'], output)

os.chdir('M:/process/pickles')
with open("riad_backup.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['GR']
for k in r:
    try: r[k]['RIAD_CHANEGID']
    except KeyError: continue
    else: 
        print k
        r[k]['RIAD_CHANGEID'] = r[k].pop('RIAD_CHANEGID')

for k, v in r.iteritems():
    for k1, v1 in v.iteritems():
        if k1 not in ['RIAD_CHANEGID']: continue
        else:
            nl = []
            for entry in v1:
                nl.append(entry[0:3] + [k] + entry[3:])
            r[k][k1] = nl
with open('riad_backup.pkl', 'wb') as output:
    cPickle.dump(riad, output)
                
pp.pprint(r['IVF7001'])
from datetime import date
r = riad['mapping']['GR']
for k, v in renameDict.iteritems():
    r[v]['RIAD_CHANEGID'] = [[k, date(2015,8,4), date(9999,12,31), datetime.now(), 'aloumiotis']] 

os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['mapping']['GR']
for k, v in r.iteritems():
    try: v['RIAD_ISMANAGEMENTOF']
    except KeyError: pass
    else:
        v['RIAD_ISMANAGEMENTOF']['GR'] = {}
        for c, cv in v['RIAD_ISMANAGEMENTOF'].items():
            if c == 'GR': continue
            v['RIAD_ISMANAGEMENTOF']['GR'][c] = [['T'] + v['RIAD_ISMANAGEMENTOF'][c][0]]
            del v['RIAD_ISMANAGEMENTOF'][c]

    try: v['MANAGEDBY']
    except KeyError: pass
    else:
        v['MANAGEDBY']['GR'] = {}
        for c, cv in v['MANAGEDBY'].items():
            if c == 'GR': continue
            v['MANAGEDBY']['GR'][c] = [['T'] + v['MANAGEDBY'][c][0]] 
            del v['MANAGEDBY'][c]

    try: v['RIAD_CHANGEEVENT']
    except KeyError: pass
    else:
        x = copy.deepcopy(v['RIAD_CHANGEEVENT'])
        del v['RIAD_CHANGEEVENT']
        v['RIAD_CHANGEEVENT'] = {}
        v['RIAD_CHANGEEVENT']['GR'] = {}
        for c in x:
            v['RIAD_CHANGEEVENT']['GR'][c[0]] = [['T', c[1], c[2], c[3], 'STAT', 'F', 'aloumiotis']]  

os.chdir('M:/process/pickles')
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)
r['1056']['BOGID']=5
r['1073']['BOGID']=37
del r['1056']['BOGID']
del r['1073']['BOGID']
r['1056']['bogid']=5
r['1073']['bogid']=37

import csv
os.chdir('M:/data/riad/test')
with open('RIAD_CHANEGID.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    fieldnames = reader.fieldnames
print fieldnames

with open('RIAD_CHANGEGID.csv', 'wb') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

with open('names.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
print 'x'
pp.pprint(r['GR']['IVF2003'])
pp.pprint(r['IVF8002'])
pp.pprint(r['1056'])
pp.pprint(r['IVF4118'])
pp.pprint(r['IVF2061'])
pp.pprint(r['AEPEY70'])
pp.pprint(r['MFMC4'])
pp.pprint(r['MFMC1001'])
pp.pprint(r['MFMC1']['RIAD_ORGUNIT'])
pp.pprint(r['AEEX1'])
pp.pprint(r['LEA2'])
pp.pprint(r['FAC101'])
r['AEPEY72'] = r.pop('AEPEY101')
r['AEPEY71'] = r.pop('AEPEY103')
r['AEPEY40'] = r.pop('AEPEY102')
r['AEPEY44'] = r.pop('AEPEY105')
r['AEPEY20'] = r.pop('AEPEY104')
pp.pprint(r['AK269'])
pp.pprint(r['AK275'])
pp.pprint(r['AK458'])
pp.pprint(r['IVF2003'])
pp.pprint(r['IVF9011'])
pp.pprint(r['IVF2061'])
pp.pprint(r['AK210'])
pp.pprint(r['FAC106'])
pp.pprint(r['CRE504'])
pp.pprint(r['MFMC20'])
pp.pprint(r['AK265'])
pp.pprint(r['AEEX1'])
print(r['AEPEY50']['GRRIAD_CTA_PRIVATE'][0][0])
pp.pprint(r['AEPEY28'])
print(r['AEPEY47']['GRRIAD_CTA_PRIVATE'][0][0])
pp.pprint(r['MFMC12'])
pp.pprint(r['LEA11'])
pp.pprint(r['MFMC1']['GRRIAD_CTA_PRIVATE'][-1][0][0][0])
print(r['MFMC1']['GRRIAD_CTA_PRIVATE'][-1][0][0][0])
pp.pprint(r['AK37'])
pp.pprint(r['AEEAP1'])
pp.pprint(r['AEEX1'])
pp.pprint(r['AK00911'])
pp.pprint(r['AK00265'])
pp.pprint(r['AEPEY002'])

os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['GR']

os.chdir('M:/process/pickles')
with open("riad_backup.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['GR']
keys = [7001, 7002, 8001, 8002, 8003, 8004, 8005]
for k, v in r.iteritems():
    if k[:5] in ['AEPEY']:
        x = v['GRRIAD_CTA_OFFICIAL']
        z = v['GRRIAD_CTA_PRIVATE']
        v['GRRIAD_CTA_OFFICIAL'] = [[[x[0][:3]]] + x[0][3:]] 
        v['GRRIAD_CTA_PRIVATE'] = [[[z[0][:3]]] + z[0][3:]] 

    if k[:3] in ['FAC', 'CRE', 'LEA']:
        x = v['GRRIAD_CTA_OFFICIAL']
        z = v['GRRIAD_CTA_PRIVATE']
        v['GRRIAD_CTA_OFFICIAL'] = [[[x[0][:3]]] + x[0][3:]] 
        v['GRRIAD_CTA_PRIVATE'] = [[[z[0][:3]]] + z[0][3:]] 

    if k[3:] in keys: 
        x = v['GRRIAD_CTA_OFFICIAL']
        z = v['GRRIAD_CTA_PRIVATE']
        v['GRRIAD_CTA_OFFICIAL'] = [[[x[0][:3]]] + x[0][3:]] 
        v['GRRIAD_CTA_PRIVATE'] = [[[z[0][:3]]] + z[0][3:]] 

r['MFMC5']['RIAD_ISMANAGEMENTOF'] = {} 
r['MFMC5']['RIAD_ISMANAGEMENTOF']['GR'] = {} 
del r['IVF2061']['RIAD_CHANGEEVENT']

for k in r:
    if k[0] in ['M', 'F', 'C', 'L']:
        r[k]['NOT_IN_RIAD'] = [2, datetime(2015,6,30)]

os.chdir('M:/process/pickles')
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

os.chdir('M:/process/pickles')
with open("riad_backup.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['GR']
for k in r.keys():
    if k[:3] in ['FAC', 'CRE', 'LEA']:
        newentry = []
        for entry in r[k]['RIAD_SECTOR']:
            new = entry[0:4] + entry[5:] 
            newentry.append(new)
        r[k]['RIAD_SECTOR'] = newentry


del r['AEPEY66']['RIAD_POSTALCODE']
del r['AEPEY70']['RIAD_ORGUNIT']
del r['LEA2']['RIAD_POSTALCODE']
del r['LEA2']['RIAD_ADDRESS']
del r['LEA2']['RIAD_CITY']

os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 

r = riad['GR']
from datetime import timedelta
from datetime import date 
os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['GR']
r['MFMC5']['NOT_IN_RIAD'] = [3, True]
pp.pprint(r['AK00219'])
pp.pprint(r['AK00253'])
print(r['AK00253']['RIAD_NAME'][0][1])
pp.pprint(r['MFMC005'])
pp.pprint(r['AK03186'])
pp.pprint(r['MFMC014'])
pp.pprint(r['AK809'])

os.chdir('M:/data/riad/2015Q2/T4')
with open('GRRIAD_SUBSECTOR.csv', 'wb') as csvfile:
    fieldnames = ['HOST', 'ID', 'STARTDATE', 'ENDDATE', 'OBS_VALUE']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerow({'ID':'AUX5001', 'HOST':'#GR', 'STARTDATE':'D2015-08-04', 'ENDDATE':'D9999-12-31', 'OBS_VALUE':'MFMC1'})
    for k in r.keys():
        if k.startswith('LEA'):

        if k in ['MFMC1001', 'AK265', 'AK809', 'MFMC5']: continue
        end = 'D9999-12-31'
        if r[k]['RIAD_ORGUNIT'][-1][2] == date(9999,12,31): start = datetime.now().date()
        else: 
            start = r[k]['RIAD_ORGUNIT'][-1][2] - timedelta(days=60)
            end = r[k]['RIAD_ORGUNIT'][-1][2]
            end = date.strftime(end, 'D%Y-%m-%d')
        start = date.strftime(start, 'D%Y-%m-%d')
        if k[:2] in ['AK']:
            if len(k)==3: num = int(k[2])
            else: num = int(k[2:])
            nk = 'AK{:05d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

        if k[:4] in ['MFMC']:
            if len(k)==5: num = int(k[4])
            else: num = int(k[4:])
            nk = 'MFMC{:03d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

        if k[:5] in ['AEPEY']:
            if len(k)==6: num = int(k[5])
            else: num = int(k[5:])
            nk = 'AEPEY{:03d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

        if k[:3] in ['LEA']:
            if len(k)==4: num = int(k[3])
            else: num = int(k[3:])
            nk = 'LEA{:03d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

        if k[:4] in ['AEEX']:
            if len(k)==5: num = int(k[4])
            else: num = int(k[4:])
            nk = 'AEEX{:03d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

        if k[:5] in ['AEEAP']:
            if len(k)==6: num = int(k[5])
            else: num = int(k[5:])
            nk = 'AEEAP{:03d}'.format(num)
            writer.writerow({'ID':k, 'HOST':'GR', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':nk})

from datetime import timedelta
from datetime import date 
os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
print riad.keys()
r = riad['GR']

os.chdir('M:/data/riad/2015Q2/T2')
for k in r.keys():
    if isinstance(r[k]['RIAD_ORGUNIT'][-1][2], datetime): r[k]['RIAD_ORGUNIT'][-1][2] = r[k]['RIAD_ORGUNIT'][-1][2].date()

os.chdir('M:/process/pickles')
with open('riad.pkl', 'wb') as output:
    cPickle.dump(riad, output)

os.chdir('M:/process/pickles')
with open("riad2.pkl", "rb") as f:
    riad = cPickle.load(f) 
print riad.keys()
r = riad['GR']
pp(r['MFMC015'])
pp(r['MFMC003'])
os.chdir('M:/process/pickles')
with open("FCL.pkl", "rb") as f:
    fcl = cPickle.load(f) 
print fcl['_Z.F_NN.A.LE.W0.S1.L.Z01.E']['LEA015']
os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['GR']
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r['CRE502'])
pp(r['AK00911'])
pp(r['AK00902'])
pp(r['AK00903'])
pp(r['AK00010'])
pp.pprint(r['AEPEY071'])
pp.pprint(r['AK00010'])
pp.pprint(r['MFMC003'])
pp.pprint(r['CRE504'])
print riad.keys()

os.chdir('M:/process/pickles')
with open("riad.pkl", "rb") as f:
    riad = cPickle.load(f) 
r = riad['GR']
map_grsubsec = {'LEA': 'S.125.C.A', 'FAC': 'S.125.C.B', 'CRE': 'S.125.C.C'}
os.chdir('M:/data/riad/2015Q2/T4')
with open('GRRIAD_SUBSECTOR.csv', 'wb') as csvfile:
    fieldnames = ['HOST', 'ID', 'SOURCE', 'STARTDATE', 'ENDDATE', 'OBS_VALUE', 'CONFIDENTIALITY']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ';', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for k in r.keys():
        for km, vm in map_grsubsec.iteritems():
            if k.startswith(km):
                start = r[k]['RIAD_ORGUNIT'][-1][1] 
                end = r[k]['RIAD_ORGUNIT'][-1][2] 
                start = date.strftime(start, 'D%Y-%m-%d')
                end = date.strftime(end, 'D%Y-%m-%d')
                writer.writerow({'ID':k, 'HOST':'GR', 'SOURCE':'STAT', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':vm, 'CONFIDENTIALITY' : 'F'})
        if k.startswith('AEPEY'):
            if r[k]['RIAD_SECTOR'][-1][1] == 'S.126.X':
                start = r[k]['RIAD_ORGUNIT'][-1][1] 
                end = r[k]['RIAD_ORGUNIT'][-1][2] 
                start = date.strftime(start, 'D%Y-%m-%d')
                end = date.strftime(end, 'D%Y-%m-%d')
                writer.writerow({'ID':k, 'HOST':'GR', 'SOURCE':'STAT', 'STARTDATE':start, 'ENDDATE':end, 'OBS_VALUE':'S.126.X.A', 'CONFIDENTIALITY': 'F'})

os.chdir('M:/process/pickles')with open("FCL.pkl", "rb") as f:
    fcl = cPickle.load(f) 
pp.pprint(fcl['_Z.F4LEASING.A.LE.W2.S11.A.Z01.E'])
pp.pprint(fcl['_Z.F4FACTORING.A.LE.W2.S11.A.Z01.E'])
print fcl[aedak.keys()[0]]

os.chdir('M:/process/pickles')
with open("AEPEY.pkl", "rb") as f:
    aepey = cPickle.load(f) 
print aepey['_Z.F522.A.F.U5.S124.A.Z01.E']
print aepey[aepey.keys()[0]]

os.chdir('M:/process/pickles')
with open("fa.pkl", "rb") as f:
    fa = cPickle.load(f) 
print fa['S126']['Q.GR.W2.S126.S1.N.A.F.F29X._Z.M']
print fa['S125']
print fa.keys()

os.chdir('M:/process/pickles')
with open("teke.pkl", "rb") as f:
    teke = cPickle.load(f) 
print teke[teke.keys()[1]]
print teke.keys()

os.chdir('M:/process/pickles')
with open("AEDAK.pkl", "rb") as f:
    aedak = cPickle.load(f) 
print ae['_Z.F522.A.F.U5.S124.A.Z01.E']
print aepey[aepey.keys()[0]]

os.chdir('M:/process/pickles')
with open("schemes.pkl", "rb") as f:
    schemes = cPickle.load(f) 
pp.pprint(schemes['META']['BOG'])
print ae['_Z.F522.A.F.U5.S124.A.Z01.E']
print aepey[aepey.keys()[0]]
os.chdir('M:/process/pickles')
with open("ecb.pkl", "rb") as f:
    ecb = cPickle.load(f) 
for k, v in ecb.iteritems():
    del v['checks']
    for k1, v1 in v.iteritems():
        if 'map' in v1: del v1['map']
import pprint as pp
pp.pprint(ecb)
up.dump_pickle('ecb', ecb, dump=True)
os.chdir('M:/process/pickles')
with open("ecb.pkl", "rb") as f:
    ecb = cPickle.load(f) 
pp.pprint(ecb)
with open("ecb.pkl", "rb") as f:
    ecb = cPickle.load(f) 
for k, v in ecb.iteritems():
    for k1, v1 in v.iteritems():
        for k2, v2 in v1.iteritems():
            ecb[k][k1][k2] = [v2] 
        print v1
    del v['checks']
    try:
        for k, v in data.iteritems():
            try:
                value = int(eval(data[k]['map'])/1000)
            except:
                logging.info('{} maps to {}'.format(k, data[k]['map']))
                raise
            else:
                try: pvalue = data[k][period['L0s']][-1][0]
                except KeyError: data[k][period['L0s']] = [[value, 'A', 'F', 'N']]
                else:
                    if pvalue == value: continue
                    else: data[k][period['L0s']].append([value, 'A', 'F', 'N'])
def x():
    return 1
minus = -1

y = (lambda z: minus*z*x())
print y(2)

os.chdir('M:/process/pickles')
with open("aepey.pkl", "rb") as f:
    aepey = cPickle.load(f) 
if '_Z.F9_NN.A.LE.W0.S1.A.Z01.E' in aepey: print True
pp.pprint(aepey['_Z.F9_NN.A.LE.W0.S1.A.Z01.E'])
print aepey.keys()
pp.pprint(aepey)
y = [1, 2, 3]
print eval(y)
def x(a, f=None):
    print b
    return a
import copy
b = {}
k=1
b[k] = [1,2,4]
sign=1
y = lambda a:sign*x(a, f=b[k])
print y(2)
sign = -1
print y(2)
k=2
y(2)

for k, v in ecb['OFI'].iteritems():
    del ecb['OFI'][k]['201506']
pp.pprint(ecb)
    for k1, v1 in v.iteritems():
        if 'map' in v1: del v1['map']

import compile
reload(compile)
compile.ecb_ts('OFI')
x = set() 
y = set([1,2,4,4])
y = y - set(x)
print y
os.chdir('r:')
# -*- coding: utf-8 -*-
aedak = 'R:\ΑΕΔΑΚ'.decode('utf8')
os.chdir(aedak)
def sum(x,y):
    return x+y
def dec(func):
    def main(x, y):
        return 'This is {}'.format(func(x, y))
    return main
@dec
def sum(x,y):
    return x+y
y = sum(2,3)
x = sum
print y
print x(4,5)
os.chdir('M:/process/pickles')
with open("fa.pkl", "rb") as f:
    fa = cPickle.load(f) 
os.chdir('M:/process/pickles')
with open("ecb.pkl", "rb") as f:
    ecb = cPickle.load(f) 
pp.pprint(ecb)
pp.pprint(fa['S126'])
for k, v in fa.iteritems():
    for k1, v1 in v.iteritems():
        del fa[k][k1]['map']
        for k2, v2 in v1.iteritems():
            ecb[k][k1][k2] = [v2] 
        print v1
    del v['checks']
    try:
        for k, v in data.iteritems():
            try:
                value = int(eval(data[k]['map'])/1000)
            except:
                logging.info('{} maps to {}'.format(k, data[k]['map']))
                raise
            else:
                try: pvalue = data[k][period['L0s']][-1][0]
                except KeyError: data[k][period['L0s']] = [[value, 'A', 'F', 'N']]
                else:
                    if pvalue == value: continue
                    else: data[k][period['L0s']].append([value, 'A', 'F', 'N'])
import 
up.dump_pickle('fa', fa, dump=False)

os.chdir('M:/process/pickles')
with open("teke.pkl", "rb") as f:
    teke = cPickle.load(f) 
teke['_Z.F_NN.A.LE.W0.S1.L.Z01.E'] =teke.pop('_Z.FN.A.LE.W0.S1.L.Z01.E')
teke['_Z.F_NN.A.LE.W0.S1.A.Z01.E'] =teke.pop('_Z.FN.A.LE.W0.S1.A.Z01.E')
up.dump_pickle('teke', teke, dump=True)
up.dump_pickle('exae', exae, dump=True)

os.chdir('M:/process/pickles')
with open("exae.pkl", "rb") as f:
    exae = cPickle.load(f) 
exae['_Z.F_NN.A.LE.W0.S1.L.Z01.E'] =exae.pop('_Z.FN.A.LE.W0.S1.L.Z01.E')
exae['_Z.F_NN.A.LE.W0.S1.A.Z01.E'] =exae.pop('_Z.FN.A.LE.W0.S1.A.Z01.E')
pp.pprint(exae)
import compile_beta as c
reload(c)
c.fa_compile('S.125', '201606')
os.chdir('M:/process/pickles')
with open("fa.pkl", "rb") as f:
    fa = cPickle.load(f) 
fa['S.125'] =fa.pop('S125') 
fa['S.126'] =fa.pop('S126') 
up.dump_pickle('fa', fa, dump=True)
pp.pprint(fa)
os.chdir('M:/process/pickles')
with open("aedak.pkl", "rb") as f:
    aedak = cPickle.load(f) 
pp.pprint(aedak['_Z.F51.A.LE.W0.S1M.L.Z01.E'])
reload(up)
schemes = up.load_main_pickle('schemes') 
pp.pprint(schemes['BOG'].keys())
oofi = up.load_dsi_pickle(
os.chdir('M:/process/pickles/prod/bog/dsi')
with open("teke.pkl", "rb") as f:
    teke = cPickle.load(f) 
for k, v in teke.iteritems():
    teke[k] = {'TEKE':teke.pop(k)}
up.dump_dsi_pickle('TEKE', teke, dump=True)
pp.pprint(teke)

pp.pprint(exae)
os.chdir('M:/process/pickles/prod/backup')
os.chdir('M:/process/pickles/prod/backup/archive/arc_2015_09_22')
with open("fa_backup.pkl", "rb") as f:
    fa = cPickle.load(f) 
for k, v in fa['S.125'].iteritems():
    if len(v['201506'])>1:
        v['201506'].pop()
        v['201506'][-1][3] = 'R'
up.dump_group_pickle('fa', fa)

pp.pprint(fa['S.125'])
pp.pprint(fa['S.125'])
for k, v in exae.iteritems():
    exae[k] = {'EXAE':exae.pop(k)}
up.dump_dsi_pickle('EXAE', exae, dump=True)
