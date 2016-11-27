# coding: utf-8
# Local Area District Brexit data query


import csv
import geoutils
import operator
import pprint
from poltical_party_utils import *

ELECTORAL_DATA_DIR = 'data/elections/'
GENELEC_DATA = "2015_election_data.csv"


def decomma(value):
    """ Get an interger value for a string with commas in """
    return 0 if value == '' else int(value.replace(',', ''))

def get_constituency_dict():
    """
        The constituency dictionary is dict with with keys being Westminster
        constituency codes, and each value being a dictionary with the
        following keys:
        - Name:         Constituency name
        - Electorate:   Electorate size
        - NumVotes:     Number of votes cast in the 2015 general election
        - VotesByParty: A dictionary with key's party short names and number
                        of votes that party received

        For example:
        cons_dict[CODEXXX] = {'Electorate': 91236,
                              'NumVotes': 64218,
                              'VotesByParty': {'G': 17227,
                                               'Other': 296,
                                               ...
                                              }
                              'Name': 'Bristol West'}
    """
    cons_dict = {}

    with open(ELECTORAL_DATA_DIR + GENELEC_DATA) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cons_dict[row['Constituency ID']] = {
                'Name': row['Constituency Name'],
                'Country': row['Country'],
                'Electorate': decomma(row['Electorate']),
                '2015NumVotes': decomma(row[' Total number of valid votes counted ']),
                '2015VotesByParty': {},
                'Biases': {}}

            def add_party(party):
                cons_dict[row['Constituency ID']]['2015VotesByParty'][party] = decomma(row[party])
                if party == LABOUR:
                    cons_dict[row['Constituency ID']]['2015VotesByParty'][party] += decomma(row['Lab Co-op'])
            for party in get_poltical_parties(row['Country']):
                add_party(party)

    for cons in cons_dict.keys():
        cons_dict[cons]['2015WinningParty'] = max(cons_dict[cons]['2015VotesByParty'].iteritems(), key=operator.itemgetter(1))[0]

        major_party_votes = sum(cons_dict[cons]['2015VotesByParty'].values())
        minor_party_votes = cons_dict[cons]['2015NumVotes'] - major_party_votes
        cons_dict[cons]['2015VotesByParty']['Other'] = minor_party_votes

    return cons_dict
CONS_d = get_constituency_dict()

def get_vote_share(country, party):
    num_of_votes_in_country = 0
    num_of_votes_for_party_in_country = 0
    for const in CONS_d.keys():
        if CONS_d[const]['Country']==country:
            num_of_votes_in_country += CONS_d[const]['2015NumVotes']
            num_of_votes_for_party_in_country += CONS_d[const]['2015VotesByParty'][party]
    percent = num_of_votes_for_party_in_country / (num_of_votes_in_country * 1.0)
    return percent
    #print "The {} vote share in {} was {}%".format(party,country,percent)


COUNTRY_DICT = {}
def get_country_vote_share():
    for country in COUNTRIES:
        COUNTRY_DICT[country] = {}
    for country in COUNTRIES:
        for party in get_poltical_parties(country):
            COUNTRY_DICT[country][party] = get_vote_share(country, party)
get_country_vote_share()
pprint.pprint(COUNTRY_DICT)

def get_biases(const):
    cons_data = CONS_d[const]
    country = cons_data['Country']
    for party in get_poltical_parties(country):
        party_vote_percent_in_const = cons_data['2015VotesByParty'][party] / (cons_data['2015NumVotes'] * 1.0)
        party_vote_percent_in_country = COUNTRY_DICT[country][party]
        bias = party_vote_percent_in_const / (party_vote_percent_in_country * 1.0)
        cons_data['Biases'][party] = bias
        #print "{} has a bias of {} towards {}".format(cons_data['Name'], party, bias)

for const in CONS_d.keys():
    get_biases(const)


from opinionpolls import opinion_polls_current


def vote_prediction(const):
    cons_data = CONS_d[const]
    country = cons_data['Country']
    cons_data['CurrentPredictVotesByParty'] = {}
    for party in get_poltical_parties(country):
        predicted_vote_percent_in_const = cons_data['Biases'][party] * opinion_polls_current[country][party]
        cons_data['CurrentPredictVotesByParty'][party] = predicted_vote_percent_in_const * cons_data['2015NumVotes']
    cons_data['PredictedWinningParty'] = max(cons_data['CurrentPredictVotesByParty'].iteritems(), key=operator.itemgetter(1))[0]
    if cons_data['PredictedWinningParty'] != cons_data['2015WinningParty']:
        print "Predict {} to go from {} to {}".format(cons_data['Name'],cons_data['2015WinningParty'],cons_data['PredictedWinningParty'])

def get_const_data_by_name(name):
    for const in CONS_d.keys():
        if name in CONS_d[const]['Name']:
            print CONS_d[const]

    return None

get_const_data_by_name('Enfield')


for const in CONS_d.keys():
    vote_prediction(const)
for party in UK_PARTIES:
    predictied_seats = len([cons for cons in CONS_d.keys() if CONS_d[cons]['PredictedWinningParty'] == party])
    print "{} are predicted {} seats".format(party, predictied_seats)



def main():
    pass
if __name__ == '__main__':
    main()
