# coding: utf-8
# Local Area District Brexit data query


import csv
import operator
import pprint
from poltical_party_utils import *


#ELECTORAL_DATA_DIR = '../brexit_election/data/elections/'
#GENELEC_DATA = "2015_election_data.csv"
ELECTORAL_DATA_DIR = '../brexit_election/data/elections/un_parsed_historicaL_election_data/'
GENELEC_DATA = "2015_old.csv"
CSV_DIRECTORY = "../brexit_election/data/elections/"
CSV_FILES = ["2001.csv","2005.csv","2010.csv"]

def decomma(value):
    """ Get an interger value for a string with commas in """
    return 0 if value == '' else int(value.replace(',', ''))
### Year   Constituency Name   Candidate Name  Party   Votes
YEARS = ['2001', '2005', '2010']
PARTIES_2001 = ['Labour']
PARTIES_2005 = ['Lab']
PARTIES_2010 = []
data = {
    '2001': {
        'count': 0.0,
        'Constituency': [],
        'Candidate': [],
        'Party': [],
        'Votes': []
    },
    '2005': {
        'count': 0.0,
        'Constituency': [],
        'Candidate': [],
        'Party': [],
        'Votes': []
    },
    '2010': {
        'count': 0.0,
        'Constituency': [],
        'Candidate': [],
        'Party': [],
        'Votes': []
    }
}

election_2001 = {
    'Constituency': [],
    'Candidate': [],
    'Party': [],
    'Votes': []
}
election_2005 = {
    'Constituency': [],
    'Candidate': [],
    'Party': [],
    'Votes': []
}
election_2010 = {
    'Constituency': [],
    'Candidate': [],
    'Party': [],
    'Votes': []
}
common_seats = []
common_seat_total_votes = []

total_votes = 0
total_lab_votes = 0
total_con_votes = 0
total_lib_votes = 0
total_green_votes = 0
total_snp_votes = 0
total_ukip_votes = 0
total_sinn_votes = 0
total_dup_votes = 0
total_sdp_votes = 0
total_plaid_votes = 0
total_uup_votes = 0
total_other_votes = 0
#def load_historic_data():
#    for csv_file in CSV_FILES:
#        with open(CSV_DIRECTORY + csv_file) as csv_data:
#            year = csv_file[:4]
#            reader = csv.DictReader(csv_data)
#            for row in reader:
#                data[year]['Constituency'] = row['Constituency Name']
#                data[year]['Candidate'] = row['Candidate']
#                data[year]['Party'] = row['Party']
#                data[year]['Votes'] = row['Votes']
#    for i in range(0,20):
#        print '2001, {0} got {1} votes in {2}\n\n'.format(data['2001']['Candidate'][i], data['2001']['Votes'][i], data['2001']['Constituency'][i])

def load_historic_data():
    for csv_file in CSV_FILES:
        with open(CSV_DIRECTORY + csv_file) as csv_data:
            year = csv_file[:4]
            reader = csv.DictReader(csv_data)
            constCounter = 0
            prev_const = ""
            for row in reader:
                if row['Candidate'] and not row['Candidate'] == ' ' :
                    res = row['Constituency Name'].find(' [')
                    if res > 0:
                        if not prev_const == row['Constituency Name'][:res]:
                            constCounter += 1
                            prev_const = row['Constituency Name'][:res]
                            # print new const name
                            #print prev_const
                        data[year]['Constituency'].append(row['Constituency Name'][:res])
                    else:
                        if not prev_const == row['Constituency Name']:
                            constCounter += 1
                            prev_const = row['Constituency Name']
                            # print new const name
                            #print prev_const
                        data[year]['Constituency'].append(row['Constituency Name'])
                    data[year]['Candidate'].append(row['Candidate'])
                    data[year]['Party'].append(row['Party'])
                    try:
                        data[year]['Votes'].append(float(row['Votes']))
                        data[year]['count'] = float(row['Votes'])+data[year]['count']
                    except TypeError, e:
                        data[year]['Votes'].append(float(0))
                        data[year]['count'] = float(0)+data[year]['count']
                    except ValueError, ev:
                        print row
            print constCounter
        same_count = 0
        curr_const = ''
        missing_2001 = 0
        missing_2005 = 0
        maybe = False
        same = False
        for each in data['2010']['Constituency']:
            if not curr_const == each:
                curr_const = each
                maybe = False
                if each not in data['2001']['Constituency']:
                    missing_2001 += 1
                    maybe = True
                    #print '2001 - ' + each
                if each not in data['2001']['Constituency']:
                    missing_2005 += 1
                    if maybe:
                        maybe = False
                        same = True
                    #print '2005 - ' + each
                if same:
                    # same disparity - worth knowing!
                    same = False
                    same_count += 1
                else:
                    # Boils down to no difference, i.e. this seat is up for grabs at all three elections.
                    common_seats.append(each)
        #print "From 2001, " + str(missing_2001) + ' seats different.'
        #print "From 2005, " + str(missing_2005) + ' seats different.'
        #print 'There were ' + str(same_count) + ' differences which were the same in 2005 and 2001.'
    #print common_seats

def get_vote_share_for_party_in_seat_in_year(seat, party, year):
    i = 0
    seat_votes = 0
    found = False
    start_i = 0
    end_i = 0
    parties = []
    respective_votes = []
    for name in data[year]['Constituency']:
        if seat == name:
            # Found the seat -  start collecting data
            found = True
            start_i = i
            parties.append(data[year]['Party'][i])
            respective_votes.append(data[year]['Votes'][i])
        else: 
            if found:
                # We're now past the seat in question - break
                end_i = (i-1)
                break
        i += 1
    seat_votes = sum(respective_votes)
    if party not in parties:
        return 0
    index = parties.index(party)
    vote_share = float(respective_votes[index])/float(seat_votes)
    return vote_share
def get_vote_share_for_party_in_year(party, year):
    total = data[year]['count']
    party_vote = 0
    i = 0
    for name in data[year]['Party']:
        vote = 0
        if name == party:
            # We should count this vote up.
            party_vote += data[year]['Votes'][i]
        i += 1
    return party_vote/total
def get_party_bias_for_seat_and_year(party, seat, year):
    national_share = get_vote_share_for_party_in_year(party, year)
    seat_share = get_vote_share_for_party_in_seat_in_year(seat, party, year)
    bias = (seat_share/national_share)-1
    return bias

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
#pprint.pprint(COUNTRY_DICT)

def get_biases(const):
    cons_data = CONS_d[const]
    country = cons_data['Country']
    for party in get_poltical_parties(country):
        party_vote_percent_in_const = cons_data['2015VotesByParty'][party] / (cons_data['2015NumVotes'] * 1.0)
        party_vote_percent_in_country = COUNTRY_DICT[country][party]
        bias = party_vote_percent_in_const / (party_vote_percent_in_country * 1.0)
        cons_data['Biases'][party] = bias
        #print "{} has a bias of {} towards {}".format(cons_data['Name'], party, bias)


from opinionpolls import opinion_polls_current


def vote_prediction(const):
    get_biases(const)
    cons_data = CONS_d[const]
    country = cons_data['Country']
    cons_data['CurrentPredictVotesByParty'] = {}
    for party in get_poltical_parties(country):
        predicted_vote_percent_in_const = cons_data['Biases'][party] * opinion_polls_current[country][party]
        cons_data['CurrentPredictVotesByParty'][party] = predicted_vote_percent_in_const * cons_data['2015NumVotes']
    cons_data['PredictedWinningParty'] = max(cons_data['CurrentPredictVotesByParty'].iteritems(), key=operator.itemgetter(1))[0]
    if cons_data['PredictedWinningParty'] != cons_data['2015WinningParty']:
        #pass
        print"Predict {} to go from {} to {}".format(cons_data['Name'],cons_data['2015WinningParty'],cons_data['PredictedWinningParty'])

def print_const_data_by_name(name):
    for const in CONS_d.keys():
        if name in CONS_d[const]['Name']:
            pass
            #pprint.pprint(CONS_d[const])
    return None
def get_constituency_data_by_name(name):
    for const in CONS_d.keys():
        if name == CONS_d[const]['Name']:
            return CONS_d[const]
    return None

def print_constituency_change_predictions():
    for const in CONS_d.keys():
        vote_prediction(const)


if __name__ == '__main__':
    load_historic_data()
    #print_constituency_change_predictions();
#for party in UK_PARTIES:
    #predictied_seats = len([cons for cons in CONS_d.keys() if CONS_d[cons]['PredictedWinningParty'] == party])
    #print "{} are predicted {} seats".format(party, predictied_seats)

#print_const_data_by_name('Bradford')


def main():
    return
    #for party in UK_PARTIES:
    #   predictied_seats = len([cons for cons in CONS_d.keys() if CONS_d[cons]['PredictedWinningParty'] == party])
    #   print "{} are predicted {} seats".format(party, predictied_seats)
if __name__ == '__main__':
    main()
