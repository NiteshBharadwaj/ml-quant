from .vol_data import VolSurfaceData, VolSmileData
import numpy as np
from datetime import timedelta

def augment_vol_data(data, n_rows, spot_perturb, time_perturb, vol_perturb):
    exis_len = len(data)
    augmented_data = []
    for i in range(0, n_rows, exis_len):
        for vol_data in data:
            perturbed_data = perturb(vol_data, spot_perturb, time_perturb, vol_perturb) if not i == 0 else vol_data
            augmented_data.append(perturbed_data)
    return augmented_data


def perturb(vol_data, strike_perturb, time_perturb, vol_perturb):
    # Only the vol is perturbed as we want to see the effect of vol.
    # So the liquid instruments' strike and expiry are kept constant
    # strike_perturb and time_perturb are ideally 0
    strikes_per = list(map(lambda x: x + strike_perturb * np.random.randn(), vol_data.strikes))
    spot_per = vol_data.spot + strike_perturb * np.random.randn()
    smiles_per = []
    for smile in vol_data.smiles:
        pillar_per = smile.pillar_date + timedelta(days = int(time_perturb * np.random.randn()))
        pert = vol_perturb * 2 * (np.random.random() - 0.5)
        vol_per = list(map(lambda x: x + pert, smile.vols))
        smile_per = VolSmileData(pillar_per, smile.rd, smile.rf, vol_per)
        smiles_per.append(smile_per)
    return VolSurfaceData(vol_data.underlying_name, vol_data.market_date,
                          vol_data.spot_date, spot_per, strikes_per, smiles_per)
