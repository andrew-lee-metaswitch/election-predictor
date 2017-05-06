LABOUR = 'Lab'
LIBDEM = 'LD'
CON = 'C'
UKIP = 'UKIP'
GREEN = 'Green'
SNP = 'SNP'
PC = 'PC'
DUP = 'DUP'
SDLP = 'SDLP'
SF = 'SF'
UUP = 'UUP'

YEARS = [1983, 1987, 1992, 1997, 2001, 2005, 2010, 2015]

LONG_NAMES = ['Labour', 'Conservative', 'Liberal Democrat', 'Scottish National', 'Plaid Cymru', 'Green', 'United Kingdom Independence', 'Independent', 'Democratic Unionist', 'Ulster Unionist', 'British National', 'Sinn Fein', 'Social Democratic and Labour']
SHORT_NAMES = ['Lab', 'Con', 'LD', 'SNP', 'PC', 'Green', 'UKIP', 'Ind', 'DUP', 'UUP', 'BNP', 'SF', 'SDLP']

ENGLAND = 'England'
SCOTLAND = 'Scotland'
WALES = 'Wales'
NI = 'Northern Ireland'
UK = 'United Kingdom'

COUNTRIES = [ENGLAND, SCOTLAND, WALES, NI]
UK_PARTIES = [LABOUR, LIBDEM, CON, UKIP, GREEN, SNP, PC, DUP, SDLP, SF, UUP]

def get_poltical_parties(country):
    MAIN_POLITICAL_PARTIES = [LABOUR, LIBDEM, CON, UKIP, GREEN]
    if country == ENGLAND:
        POLITICAL_PARTIES = MAIN_POLITICAL_PARTIES
    if country == SCOTLAND:
        POLITICAL_PARTIES = MAIN_POLITICAL_PARTIES + [SNP]
    if country == WALES:
        POLITICAL_PARTIES = MAIN_POLITICAL_PARTIES + [PC]
    if country == NI:
        POLITICAL_PARTIES = [DUP, SDLP, SF, UUP]
    if country == UK:
        POLITICAL_PARTIES = UK_PARTIES
    return POLITICAL_PARTIES