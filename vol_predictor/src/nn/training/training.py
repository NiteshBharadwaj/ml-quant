import torch
import os
from tqdm import tqdm
import numpy as np
from visualization.visualize_vol_surface import visualize_vol_surface_overlap


def step(data_loader, model, criterion, to_train=False, optimizer=None):
    if to_train:
        model.train()
    else:
        model.eval()
    nIters = len(data_loader)
    loss_meter, err_meter = AverageMeter(), AverageMeter()
    with tqdm(total=nIters) as t:
        for i, (input_, gt_, mean, std, index) in enumerate(data_loader):
            input_var = torch.autograd.Variable(input_).float().cuda()
            gt_var = torch.autograd.Variable(gt_).float().cuda()
            output = model(input_var)
            loss = criterion(output, gt_var)
            if to_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            loss_meter.update(loss.data.cpu().numpy())
            output_unnorm = unnorm(output.data.cpu().numpy(), mean, std)
            gt_unnorm = unnorm(gt_var.data.cpu().numpy(), mean, std)
            vol_err = np.abs(output_unnorm - gt_unnorm).mean()
            err_meter.update(vol_err.numpy())
            t.set_postfix(loss='{:05.3f}'.format(loss_meter.avg), vol_err='{:05.3f}'.format(err_meter.avg))
            t.update()
    return loss_meter.avg, err_meter.avg


def train_model(train_loader, test_loader, model, loss, n_epochs, val_interval, learn_rate, drop_lr, save_dir):
    optimizer = torch.optim.Adam(model.parameters(), learn_rate)
    loss_avg, err_avg = 0.0, 0.0
    for epoch in range(1, n_epochs + 1):
        step(train_loader, model, loss, True, optimizer)
        if epoch % val_interval == 0:
            loss_avg, err_avg = step(test_loader, model, loss)
            torch.save(model, os.path.join(save_dir, 'model_{}.pth'.format(epoch)))
        adjust_learning_rate(optimizer, epoch, drop_lr, learn_rate)
    return loss_avg, err_avg


def test_model(test_loader, model, loss):
    loss_avg, err_avg = step(test_loader, model, loss)
    return loss_avg, err_avg


def visualize_res(test_loader, model, saveDir, indices=[0]):
    model.eval()
    annot = test_loader.dataset.annot
    nStrikes = annot['grid_size_str']
    nMats = annot['grid_size_mat']
    for idx in indices:
        input_, gt_, mean, std, _ = test_loader.dataset[idx]
        input_var = torch.autograd.Variable(torch.from_numpy(input_.reshape(1, input_.shape[0]))).float().cuda()
        gt_var = torch.autograd.Variable(torch.from_numpy(gt_.reshape(1, gt_.shape[0]))).float().cuda()
        output = model(input_var)
        output_unnorm = unnorm(output.data.cpu().numpy(), mean, std)
        gt_unnorm = unnorm(gt_var.data.cpu().numpy(), mean, std)
        output_unnorm = output_unnorm.reshape(nMats, nStrikes)
        gt_unnorm = gt_unnorm.reshape(nMats, nStrikes)
        strike_high = annot['strike_high'][idx]
        strike_low = annot['strike_low'][idx]
        start_time = annot['start_time'][idx]
        end_time = annot['end_time'][idx]
        visualize_vol_surface_overlap(output_unnorm, gt_unnorm, strike_low, strike_high,
                                      start_time, end_time, nStrikes, nMats, saveDir)


def unnorm(output, mean, std):
    return output * std + mean


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def adjust_learning_rate(optimizer, epoch, dropLR, LR):
    lr = LR * (0.1 ** (epoch // dropLR))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
