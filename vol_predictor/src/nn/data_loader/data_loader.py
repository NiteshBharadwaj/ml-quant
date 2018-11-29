import torch.utils.data as data
from h5py import File
import numpy as np


class DataLoader_Surface(data.Dataset):
    def __init__(self, annot_file, split, tr_percent = 0.7):
        print('Initializing data loader {}  from {}'.format(split, annot_file))
        f = File(annot_file, 'r')
        keys = [key for key in f.keys()]
        annot = {}
        for key in keys:
            annot[key] = np.asarray(f[key]).copy()
        f.close()
        # Keys: input, output, strike_low, strike_high, start_time, end_time, grid_size_str, grid_size_mat

        full_data_len = annot['input'].shape[0]
        ids = np.arange(full_data_len)
        max_id_te = int((1 - tr_percent) * full_data_len)
        te_ids = ids[ids < max_id_te]
        tr_ids = ids[ids >= max_id_te]

        self.tr_mean_inp = annot['input'][tr_ids].mean(axis=0)
        self.tr_std_inp = annot['input'][tr_ids].std(axis=0)
        annot['input'] = (annot['input'] - self.tr_mean_inp) / (self.tr_std_inp + 1e-8)
        self.tr_mean_opt = annot['output'][tr_ids].mean(axis=0)
        self.tr_std_opt = annot['output'][tr_ids].std(axis=0)
        annot['output'] = (annot['output'] - self.tr_mean_opt) / (self.tr_std_opt + 1e-8)

        for key in keys:
            if not annot[key].shape == ():
                annot[key] = annot[key][tr_ids if split=='train' else te_ids]

        self.annot = annot
        self.nSamples = annot['input'].shape[0]
        print('Loaded {} {} samples'.format(split, self.nSamples))

    def __getitem__(self, index):
        return self.annot['input'][index].copy(), self.annot['output'][index].copy(), self.tr_mean_opt, self.tr_std_opt, index

    def __len__(self):
        return self.nSamples


class DataLoader_Point(DataLoader_Surface):
    def __init__(self, annot_file, split, tr_percent=0.7):
        super().__init__(annot_file, split, tr_percent)
        opt = self.annot['output']
        self.nStrikes = self.annot['grid_size_str']
        self.nMats = self.annot['grid_size_mat']
        self.annot['output'] = opt.reshape(opt.shape[0], self.nMats, self.nStrikes)
        self.tr_mean_opt = self.tr_mean_opt.reshape(self.nMats, self.nStrikes)
        self.tr_std_opt = self.tr_std_opt.reshape(self.nMats, self.nStrikes)

    # Probabilistic data loader
    def __getitem__(self, index):
        strike_id = np.random.randint(self.nStrikes)
        time_id = np.random.randint(self.nMats)
        strike_step = (self.annot['strike_high'][index] - self.annot['strike_low'][index]) / self.nStrikes
        time_step = (self.annot['end_time'][index] - self.annot['start_time'][index]) / self.nMats
        strike = self.annot['strike_low'][index] + strike_id * strike_step
        mat = self.annot['start_time'][index] + time_id * time_step
        vol = self.annot['output'][index, time_id, strike_id]

        nInp_raw = self.annot['input'][index].shape[0].copy()
        nInp = nInp_raw + 2
        inp = np.zeros(nInp)
        inp[0 : nInp_raw] = self.annot['input'][index]
        inp[nInp_raw] = strike
        inp[nInp_raw + 1] = mat

        mean = self.tr_mean_opt[time_id, strike_id]
        std = self.tr_std_opt[time_id, strike_id]

        return inp, vol, mean, std, index
