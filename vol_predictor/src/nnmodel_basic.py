from opts.nnmodel_opts import NNModelOpts
from nn.data_loader.data_loader_utils import create_data_loaders
from nn.model.nnmodel_utils import create_model
from nn.training.training import train_model, test_model, visualize_res
import numpy as np
import torch
import random

def main():
    # Seed all sources of randomness to 0 for reproducibility
    np.random.seed(0)
    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    random.seed(0)

    opt = NNModelOpts().parse()
    train_loader, test_loader = create_data_loaders(opt)
    model, loss = create_model(opt, train_loader.dataset[0])
    if not opt.loadModel == 'none':
        model = torch.load(opt.loadModel).cuda()
    if opt.train:
        train_model(train_loader, test_loader, model, loss, opt.nEpochs, opt.valInterval, opt.LR, opt.dropLR, opt.saveDir)
    loss_stat, vol_err_stat = test_model(test_loader, model, loss)
    print('Test loss: ' + str(loss_stat))
    print('Test vol: ' + str(vol_err_stat))
    #print('Pricing error: ' + str(vol_err_stat) + ' USD per underlying unit')
    visualize_res(test_loader, model, opt.saveDir)

if __name__ == '__main__':
    main()
