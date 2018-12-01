from data_process.parse_vol_data import parse_vol_data
from data_process.augment_vol_data import augment_vol_data
from data_process.create_gt import flatten_surface
from vol_models.calc_utils import get_vol_model, create_vol_grid
from opts.volmodel_opts import VolModelOpts
import os
import h5py
import numpy as np
import random


def create_gt(opt):
    # Seed all sources of randomness to 0 for reproducibility
    np.random.seed(0)
    random.seed(0)

    # Read opts
    data = opt.data
    n_rows = opt.nRows
    grid_size = opt.gridSize
    strike_perturb = opt.strikePerturb
    time_perturb = opt.matPerturb
    vol_perturb = opt.volPerturb

    # Parse CSV data
    data_parsed = parse_vol_data(data)

    # Augment data to reach the number of rows required
    data_augmented = augment_vol_data(data_parsed, n_rows, strike_perturb, time_perturb, vol_perturb)

    # Get vol model function
    vol_model_fn = get_vol_model(opt.volModel)

    annot = {}
    annot['input'] = []
    annot['output'] = []
    annot['strike_low'] = []
    annot['strike_high'] = []
    annot['start_time'] = []
    annot['end_time'] = []
    annot['id'] = []
    id = -1
    for vol_data in data_augmented:
        try:
            id += 1
            # Get vol model
            vol_surface = vol_model_fn(vol_data)
            # Calibrate vol surface
            calibrated_vol, strike_low, strike_high, start_time, end_time = \
                create_vol_grid(vol_surface, grid_size, grid_size)

            spot = vol_data.spot
            # Flatten surface
            input_, output = flatten_surface(vol_data, calibrated_vol)

            annot['input'].append(input_)
            annot['output'].append(output)
            annot['strike_low'].append(strike_low/spot)
            annot['strike_high'].append(strike_high/spot)
            annot['start_time'].append(start_time)
            annot['end_time'].append(end_time)
            annot['grid_size_str'] = grid_size
            annot['grid_size_mat'] = grid_size
            annot['id'].append(id)
        except:
            # Calibration failed
            continue
    return annot


def save_annot(annot, opt, annot_name):
    fname = os.path.join(os.path.split(opt.data)[0], opt.volModel + '_' + annot_name)
    data_file = h5py.File(fname, 'w')
    for key in annot.keys():
        data_file[key] = annot[key]
    data_file.close()
    nIds = len(annot['id'])
    print('Saved {} samples as annot to {}'.format(nIds, fname))


def main():
    opt = VolModelOpts().parse()
    annot = create_gt(opt)
    save_annot(annot, opt, 'annot.h5')


if __name__ == '__main__':
    main()
