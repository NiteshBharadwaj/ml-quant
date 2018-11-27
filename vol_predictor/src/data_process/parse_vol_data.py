import csv
from .vol_data import VolSurfaceData, VolSmileData
from dateutil.parser import parse as parse_date


# Parser for a particular format of csv data input
# underlying_name, market_date, spot_date, spot, n_strikes, strike_1, strike_2, ..., strike_n_strikes
# (pillar_date, rd, rf,
#   vol_1, vol_2, ..., vol_n_strikes)...
def parse_vol_data(data_dir):
    with open(data_dir, 'r') as csvfile:
        vol_data_txt_file = csv.reader(csvfile)
        vol_data_arr = []
        for vol_data_txt in vol_data_txt_file:
            smiles = []
            i = 4
            n_strikes = int(vol_data_txt[i])
            i = i + 1
            strikes = []
            for j in range(n_strikes):
                strikes.append(float(vol_data_txt[i + j]))
            i = i + n_strikes
            while i < len(vol_data_txt):
                if vol_data_txt[i] == '':
                    break
                pillar_date = parse_date(vol_data_txt[i], dayfirst=True)
                rd = float(vol_data_txt[i + 1])
                rf = float(vol_data_txt[i + 2])
                i = i + 3
                vols = []
                for j in range(n_strikes):
                    vols.append(float(vol_data_txt[i + j]))
                i = i + n_strikes
                smiles.append(
                    VolSmileData(pillar_date, rd, rf, vols))
            vol_data = VolSurfaceData(vol_data_txt[0], parse_date(vol_data_txt[1], dayfirst=True),
                                      parse_date(vol_data_txt[2], dayfirst=True), float(vol_data_txt[3]), strikes, smiles)
            vol_data_arr.append(vol_data)
        return vol_data_arr
