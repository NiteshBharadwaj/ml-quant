import numpy as np

def flatten_surface(vol_data, vol_surface):
    # time_1, time_2 , ... time_n, rd_1, rd_2,....,rd_n, rf_1,...,rf_n, strike_1, strike_2,... strike_m,   vol_11, vol12,..., vol_nm
    market_date = vol_data.market_date
    spot = vol_data.spot
    strikes = list(map(lambda x: x / spot, vol_data.strikes))
    smiles = vol_data.smiles
    mats = list(map(lambda x: (x.pillar_date - market_date).days/365.0, smiles))
    rds = list(map(lambda x: x.rd, smiles))
    rfs = list(map(lambda x: x.rf, smiles))
    nStrikes = len(strikes)
    nMat = len(smiles)
    flat_input = np.zeros(nMat*nStrikes + 3*nMat + nStrikes) - 1
    i = 0
    flat_input[i:i + nMat] = mats
    i = i + nMat
    flat_input[i:i + nMat] = rds
    i = i + nMat
    flat_input[i:i + nMat] = rfs
    i = i + nMat
    flat_input[i:i + nStrikes] = strikes
    i = i + nStrikes
    for smile in smiles:
        flat_input[i: i + nStrikes] = smile.vols
        i = i + nStrikes
    assert ((flat_input<0).sum()==0)
    return flat_input, vol_surface['vols'].flatten()

