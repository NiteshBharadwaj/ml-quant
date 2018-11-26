import csv

def parse_vol_data(dataDir):
    with open(dataDir, 'rb') as csvfile:
        vol_data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in vol_data:
        print(', '.join(row))