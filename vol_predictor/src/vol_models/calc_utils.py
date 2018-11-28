import numpy as np
from vol_models.black_cubic import BlackCubic
from vol_models.dupire_local import DupireLocal
from vol_models.heston_slv import HestonSLV

def get_vol_model(vol_model_str):
    if vol_model_str == 'black_cubic':
        return lambda x: BlackCubic(x)
    elif vol_model_str == 'dupire_local':
        return lambda x: DupireLocal(x)
    elif vol_model_str == 'heston_slv':
        return lambda x: HestonSLV(x)


def create_vol_grid(vol_surface, grid_size_str, grid_size_time):
    strike_low = min(vol_surface.strikes)
    strike_high = max(vol_surface.strikes)
    start_time = min(map(lambda x: (x - vol_surface.calculation_date) / 365.0, vol_surface.expiration_dates))
    end_time = max(map(lambda x: (x - vol_surface.calculation_date) / 365.0, vol_surface.expiration_dates))
    strike_step = (strike_high - strike_low) / grid_size_str
    time_step = (end_time - start_time) / grid_size_time
    times = np.arange(start_time, end_time, time_step)
    strikes = np.arange(strike_low, strike_high, strike_step)
    X, Y = np.meshgrid(times, strikes)
    Z = np.array([vol_surface.get_vol(y, x)
                  for xr, yr in zip(X, Y)
                  for x, y in zip(xr, yr)]
                 ).reshape(len(X), len(X[0]))
    calibrated = {'strikes': Y, 'times': X, 'vols': Z}
    return calibrated, strike_low, strike_high, start_time, end_time
