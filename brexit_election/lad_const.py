# coding: utf-8
"""
    lad.py

    Local Area District Brexit data query
"""

from collections import namedtuple
import logging
import csv
import geoutils
import operator

ELECTORAL_DATA_DIR = 'data/elections/'
BREXIT_DATA = "brexit_election_data.csv"
GENELEC_DATA = "2015_election_data.csv"


def decomma(value):
    """ Get an interger value for a string with commas in """
    return 0 if value == '' else int(value.replace(',', ''))


def get_lad_code_dict():
    """
        lad_dict is a dictionary with keys being LAD Codes, and each value
        being a dictionary with the following keys:
        - Area: area name
        - Electorate: Electorate size
        - Remain: Size of reamin vote
        - Leave: Size of Leave vote
        - Result: Either 'Remain' or 'leave', whichever won

        For example:
        lad_dict[CODEXXX] = {'Electorate': 312465,
                             'Leave': 87418,
                             'Remain': 141027,
                             'Result': 'Remain',
                             'Area': 'Bristol, City of'}
    """
    lad_dict = {}
    with open(ELECTORAL_DATA_DIR + BREXIT_DATA) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lad_dict[row['Area_Code']] = {'Area': row['Area'],
                                          'Electorate': int(row['Electorate']),
                                          'Remain': int(row['Remain']),
                                          'Leave' : int(row['Leave']), }

    for lad in lad_dict.keys():
        if lad_dict[lad]['Remain'] > lad_dict[lad]['Leave']:
            lad_dict[lad]['Result'] = 'Remain'
        else:
            lad_dict[lad]['Result'] = 'Leave'

    return lad_dict


def get_constituency_dict():
    cons_dict = {}

    with open(ELECTORAL_DATA_DIR + GENELEC_DATA) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cons_dict[row['Constituency ID']] = {
                'Name': row['Constituency Name'],
                'Electorate': decomma(row['Electorate']),
                'NumVotes': decomma(row[' Total number of valid votes counted '])}
            def add_party(party):
                cons_dict[row['Constituency ID']]['VotesByParty'][party] = decomma(row[party])
            for party in ['Lab','C','LD','Green','UKIP','SNP','DUP','SDLP','SF','UUP','PC']:
                add_party(party)

    for cons in cons_dict.keys():
        cons_dict[cons]['WinningParty'] = max(cons_dict[cons]['VotesByParty'].iteritems(), key=operator.itemgetter(1))[0]

        major_party_votes = sum(cons_dict[cons]['VotesByParty'].values())
        minor_party_votes = cons_dict[cons]['NumVotes'] - major_party_votes
        cons_dict[cons]['VotesByParty']['Other'] = minor_party_votes
        cons_dict[cons]['LAD'] = geoutils.get_area_overlap(cons)
    return cons_dict

# At this point const dict is a dictinoary with keys being Const. Codes, and each value being a dictionary with the following keys:
#   Name: Const  name
#   Electorate: Electorate size
#   NoVotes: No of votes cast
#   VotesByParty: A dictioanry with key's party short names and number of votes of
#   e.g. cons_dict[CODEXXX]=
#  {'Electorate': 91236, 'NoVotes': 64218, 'VotesByParty':
#  {'G': 17227, 'Other': 296, 'DUP': 0, 'Con': 9752, 'LD': 12103, 'SDLP': 0,
#  'UKIP': 1940, 'UUP': 0, 'Lab': 22900, 'PC': 0, 'SNP': 0, 'SF': 0}, 'Name': 'Bristol West'}



if __name__ == '__main__':
    main()
