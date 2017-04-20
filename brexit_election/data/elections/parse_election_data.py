import os, sys, re, xlrd, csv
import unicodedata

def reunicode_cell(a,b):

    cell = sh.cell(a,b).value
    try:
        return str(cell)
    except:
        return unicodedata.normalize('NFKD', cell).encode('ascii','ignore')

con_reg = re.compile('^[A-Z].* \[\d{1,3}\]$')
con_reg_2001 = re.compile('^[A-Z].*$')
def get_2010_data():
    excel_file_2010 = os.path.join('un_parsed_historical_election_data','2010.xls')

    wb = xlrd.open_workbook(excel_file_2010)
    sh = wb.sheet_by_index(0)
    i = 1
    with open("2010.csv", "wb") as output_file:
        csv_file = csv.writer(output_file, delimiter=',',
                   quoting=csv.QUOTE_ALL)
        while i <= sh.nrows:
            print sh.cell(i,0).value
            if re.match(con_reg, reunicode_cell(i,0)):

               cons =  reunicode_cell(i,0)
               print cons
               i += 1
            elif reunicode_cell(i,4) == '-----':
                   i += 2
            else:
                candidate = reunicode_cell(i,2)
                party = reunicode_cell(i,3)
                votes = reunicode_cell(i,4)
                csv_file.writerow(['2010', cons, candidate, party, votes])
                i += 1


def get_2005_data():

    i = 12
    with open("2005.csv", "wb") as output_file:
        csv_file = csv.writer(output_file, delimiter=',',
                              quoting=csv.QUOTE_ALL)
        while i <= sh.nrows:
            print sh.cell(i, 0).value
            if reunicode_cell(i, 4) == '-----':
                i += 3
            else:
                if re.match(con_reg, reunicode_cell(i, 0)):
                    cons = reunicode_cell(i, 0)
                    print cons
                candidate = reunicode_cell(i, 2)
                party = reunicode_cell(i, 3)
                votes = reunicode_cell(i, 4)
                csv_file.writerow(['2005', cons, candidate, party, votes])
                i += 1

def get_2001_data():

    i = 2
    with open("2001.csv", "wb") as output_file:
        csv_file = csv.writer(output_file, delimiter=',',
                              quoting=csv.QUOTE_ALL)
        while i <= sh.nrows:
            print sh.cell(i, 0).value
            if reunicode_cell(i, 4) == '':
                i += 1
            else:
                if re.match(con_reg_2001, reunicode_cell(i, 0)):
                    cons = reunicode_cell(i, 0)
                    print cons
                candidate = reunicode_cell(i, 2)
                party = reunicode_cell(i, 3)
                votes = reunicode_cell(i, 4)
                csv_file.writerow(['2001', cons, candidate, party, votes])
                i += 1

def get_2015_data():
    excel_file_2015 = os.path.join('un_parsed_historical_election_data', '2015.xlsx')
    i = 2
    with open("2015.csv", "wb") as output_file:
        csv_file = csv.writer(output_file, delimiter=',',
                              quoting=csv.QUOTE_ALL)
        while i <= sh.nrows:
            cons - reunicode_cell(i,2)
            #Lab
            candidate = reunicode_cell(i, 2)
            party = reunicode_cell(i, 3)
                votes = reunicode_cell(i, 4)
                csv_file.writerow(['2001', cons, candidate, party, votes])
                i += 1


excel_file_2015 = os.path.join('un_parsed_historical_election_data', '2015.xlsx')
wb = xlrd.open_workbook(excel_file_2015)
sh = wb.sheet_by_index(0)
get_2015_data()