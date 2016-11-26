
# coding: utf-8

# In[29]:

# lad.py
# Local Area District Brexit data query

from collections import namedtuple
import logging
import csv
import geoutils

lad_csv_data = "brexit_election_data.csv"
lad_dict = {}
with open(lad_csv_data) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lad_dict[row['Area_Code']] = {'Area': row['Area'],
                                     'Electorate': int(row['Electorate']),
                                     'Remain': int(row['Remain']),
                                     'Leave' : int(row['Leave']), }
        
        #print lad_dict[row['Area_Code']] 
for lad in lad_dict.keys():
    if lad_dict[lad]['Remain'] > lad_dict[lad]['Leave']:
        lad_dict[lad]['Result'] = 'Remain'
    else:
        lad_dict[lad]['Result'] = 'Leave'
       
       
# At this point lad_dict is a dictinoary with keys being LAD Codes, and each vlaue being a dictionary with the following keys:
#   Area: area name
#   Electorate: Electorate size
#   Reamin: Size of reamin vote
#   Leave: Size of Leave vote
#   Result: Either 'Remain' or 'leave', whichever won
#   e.g. lad_dict[CODEXXX]= 
#  {'Electorate': 312465, 'Leave': 87418, 'Remain': 141027, 'Result': 'Remain', 'Area': 'Bristol, City of'}


# In[45]:

cons_csv_data = "2015_election_data.csv"
cons_dict = {}
import operator
def decomma(value):
    if value == '':
        return 0
    else:
        return int(value.replace(',', ''))

with open(cons_csv_data) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cons_dict[row['Constituency ID']] = {
            'Name': row['Constituency Name'],
            'Electorate': decomma(row['Electorate']),
            'NoVotes': decomma(row[' Total number of valid votes counted '])}
        cons_dict[row['Constituency ID']]['VotesByParty'] = {
            'Lab' : decomma(row['Lab']),
            'Con' : decomma(row['C']),
            'LD' : decomma(row['LD']),
            'G' : decomma(row['Green']),
            'UKIP' : decomma(row['UKIP']),
            'SNP' : decomma(row['SNP']),
            'DUP' : decomma(row['DUP']),
            'SDLP' : decomma(row['SDLP']),
            'SF' : decomma(row['SF']),
            'UUP' : decomma(row['UUP']),
            'PC' : decomma(row['PC']),}
        

        
        #print lad_dict[row['Area_Code']] 
for cons in cons_dict.keys():
    cons_dict[cons]['WinningParty'] = max(cons_dict[cons]['VotesByParty'].iteritems(), key=operator.itemgetter(1))[0]
    
    major_party_votes = sum(cons_dict[cons]['VotesByParty'].values())
    minor_party_votes = cons_dict[cons]['NoVotes'] - major_party_votes
    cons_dict[cons]['VotesByParty']['Other'] = minor_party_votes
    if 'Bristol' in cons_dict[cons]['Name']:
        print cons_dict[cons]
    cons_dict[cons]['LAD'] = geoutils.get_area_overlap(cons)
        
# At this point const dict is a dictinoary with keys being Const. Codes, and each value being a dictionary with the following keys:
#   Name: Const  name
#   Electorate: Electorate size
#   NoVotes: No of votes cast
#   VotesByParty: A dictioanry with key's party short names and number of votes of 
#   e.g. cons_dict[CODEXXX]= 
#  {'Electorate': 91236, 'NoVotes': 64218, 'VotesByParty':
#  {'G': 17227, 'Other': 296, 'DUP': 0, 'Con': 9752, 'LD': 12103, 'SDLP': 0, 
#  'UKIP': 1940, 'UUP': 0, 'Lab': 22900, 'PC': 0, 'SNP': 0, 'SF': 0}, 'Name': 'Bristol West'}


# In[ ]:

for cons in cons_dict:
    


# In[ ]:



