from .vol_data import VolSurfaceData, VolSmileData
import numpy as np
from datetime import timedelta

def augment_vol_data(data, n_rows, spot_perturb, time_perturb, vol_perturb):
    exis_len = len(data)
    augmented_data = []
    for i in range(0, n_rows, exis_len):
        for vol_data in data:
            perturbed_data = perturb_gauss(vol_data, spot_perturb, time_perturb, vol_perturb) if not i == 0 else vol_data
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


# Subtracts bivariate gaussian, centered at random point, from input data
def perturb_gauss(vol_data, strike_perturb, time_perturb, vol_perturb, n_gauss = 5):
    # Only the vol is perturbed as we want to see the effect of vol.
    # So the liquid instruments' strike and expiry are kept constant
    # strike_perturb and time_perturb are ideally 0
    strikes_per = list(map(lambda x: x + strike_perturb * np.random.randn(), vol_data.strikes))
    spot_per = vol_data.spot + strike_perturb * np.random.randn()
    n_strikes = len(vol_data.strikes)
    n_mats = len(vol_data.smiles)
    vols_coll = np.zeros((n_mats, n_strikes))
    i = 0
    for smile in vol_data.smiles:
        vols_coll[i] = smile.vols
        i += 1
    for j in range(n_gauss):
        z = get_bivariate_normal(n_strikes, n_mats, vol_perturb)
        vols_coll = vols_coll - z
    smiles_per = []
    i = 0
    for smile in vol_data.smiles:
        pillar_per = smile.pillar_date + timedelta(days = int(time_perturb * np.random.randn()))
        vol_per = vols_coll[i]
        smile_per = VolSmileData(pillar_per, smile.rd, smile.rf, vol_per)
        smiles_per.append(smile_per)
        i += 1
    return VolSurfaceData(vol_data.underlying_name, vol_data.market_date,
                          vol_data.spot_date, spot_per, strikes_per, smiles_per)


def get_bivariate_normal(n_strikes, n_mats, vol_perturb):
    x, y = np.meshgrid(np.linspace(-1, 1, n_strikes), np.linspace(-1, 1, n_mats))
    mu_x = 2 * (np.random.random() - 0.5)
    mu_y = 2 * (np.random.random() - 0.5)
    p = 2 * (np.random.random() - 0.5)
    z = bivariate_normal(x, y, 1.0, 1.0, mu_x, mu_y, sigmaxy=p)
    z = (z - z.mean()) / z.std() * vol_perturb * 0.3 #Rescale pdf so that  vol is in reasonable range (-5% to 5%)
    return z


def bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0,
                     mux=0.0, muy=0.0, sigmaxy=0.0):
    """
    Bivariate Gaussian distribution for equal shape *X*, *Y*.

    See `bivariate normal
    <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
    at mathworld.
    """
    Xmu = X-mux
    Ymu = Y-muy

    rho = sigmaxy/(sigmax*sigmay)
    z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
    denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
    return np.exp(-z/(2*(1-rho**2))) / denom

