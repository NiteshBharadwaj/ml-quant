from nn.model.nnmodel import Linear
import torch.nn as nn


def create_model(opt, sample_data):
    model_name = opt.nnModel
    if model_name == 'linear':
        inp_size = sample_data[0].shape[0]
        opt_size = sample_data[1].shape[0]
        return Linear(inp_size, opt_size).cuda(), nn.MSELoss().cuda()
    else:
        raise ValueError('Model ' + model_name + ' not recognized.')
