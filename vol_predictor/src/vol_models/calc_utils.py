import numpy as np
from vol_models.black_cubic import BlackCubic
from vol_models.dupire_local import DupireLocal
from vol_models.heston_slv import HestonSLV
from visualization.visualize_vol_surface import visualize_vol_surface_calibrated


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
    Z = np.zeros((strikes.shape[0], times.shape[0]))
    for i in range(times.shape[0]):
        for j in range(strikes.shape[0]):
            strike = strikes[j]
            time = times[i]
            Z[j, i] = vol_surface.get_vol(strike, time, True) if j == 0 else vol_surface.get_vol(strike, time, False)
    calibrated = {'strikes': Y, 'times': X, 'vols': Z}
    # visualize_vol_surface_calibrated(calibrated, strikes, times)
    return calibrated, strike_low, strike_high, start_time, end_time
