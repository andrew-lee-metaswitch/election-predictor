# coding: utf-8
# Local Area District Brexit data query


import csv
import geoutils
import operator

ELECTORAL_DATA_DIR = 'data/elections/'
BREXIT_DATA = "brexit_election_data.csv"
BREXIT_DATA_NI = "brexit_northern_ireland_breakdown.csv"
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
            if row['Area_Code'] not in ['GI', 'N92000002']:
                lad_dict[row['Area_Code']] = {'Area': row['Area'],
                                              'Electorate': int(row['Electorate']),
                                              'Remain': int(row['Remain']),
                                              'Leave' : int(row['Leave']), }

    with open(ELECTORAL_DATA_DIR + BREXIT_DATA_NI) as csvfile:
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
                'Electorate': decomma(row['Electorate']),
                'NumVotes': decomma(row[' Total number of valid votes counted ']),
                'VotesByParty': {}}

            def add_party(party):
                cons_dict[row['Constituency ID']]['VotesByParty'][party] = decomma(row[party])
            for party in ['Lab','C','LD','Green','UKIP','SNP','DUP','SDLP','SF','UUP','PC']:
                add_party(party)

    for cons in cons_dict.keys():
        cons_dict[cons]['WinningParty'] = max(cons_dict[cons]['VotesByParty'].iteritems(), key=operator.itemgetter(1))[0]

        major_party_votes = sum(cons_dict[cons]['VotesByParty'].values())
        minor_party_votes = cons_dict[cons]['NumVotes'] - major_party_votes
        cons_dict[cons]['VotesByParty']['Other'] = minor_party_votes

    return cons_dict

LAD_d = get_lad_code_dict()
CONS_d = get_constituency_dict()

def is_brexit_party(party):
    brexit_party = True
    if party in ['Lab','LD','Green','SNP','SDLP','SF','PC']:
        brexit_party = False
    return brexit_party

def voted_for_brexit(const):
    cons_data = CONS_d[const]
    lads = cons_data['LAD']
    estimate_of_electorate_size = 0
    estimate_of_remain_voters = 0
    estimate_of_leave_voters = 0
    for lad in lads.keys():
        lad_data = LAD_d[lad]
        # This is an estimate of the number of people in the constinuency who can vote who can live
        # in this LAD
        ele_size = int(lads[lad] * lad_data['Electorate'])
        # Based on the number of remain voters in this LAD, we add that many remain voters to the
        # estimate_of_remain_voters in that constitenucy
        estimate_of_remain_voters += (ele_size * lad_data['Remain']) / lad_data['Electorate'] * 1.0
        estimate_of_leave_voters += (ele_size * lad_data['Leave']) / lad_data['Electorate'] * 1.0
        estimate_of_electorate_size += ele_size
    vote_outcome = 'Leave'
    if estimate_of_remain_voters > estimate_of_leave_voters:
        vote_outcome = 'Remain'
    return vote_outcome


def main():
    leave = 0
    remain = 0

    for const in CONS_d.keys():
        cons_data = CONS_d[const]
        cons_data['LAD'] = geoutils.get_area_overlap(const)
        outcome = voted_for_brexit(const)

        print "{} voted for {} at the 2015 election, " \
              "they voted {} in Brexit vote".format(cons_data['Name'], cons_data['WinningParty'], outcome)

        if outcome == 'Leave':
            leave += 1
        elif outcome == 'Remain':
            remain += 1
        else:
            assert False

    print "Final tally: Leave - %s, Remain - %s" % (str(leave), str(remain))


if __name__ == '__main__':
    main()
