from nn.data_loader.data_loader import DataLoader_Surface, DataLoader_Point
import torch


def create_data_loaders(opt):
    tr_dataset, te_dataset = create_data_sets(opt)
    train_loader = torch.utils.data.DataLoader(
        tr_dataset,
        batch_size=opt.batchSize,
        shuffle=True if opt.DEBUG == 0 else False,
        drop_last=True,
        num_workers=opt.nThreads
    )
    test_loader = torch.utils.data.DataLoader(
        te_dataset,
        batch_size=opt.batchSize,
        shuffle=False,
        num_workers=opt.nThreads
    )
    return train_loader, test_loader


def create_data_sets(opt):
    train_type = opt.trainType
    annot_file = opt.data
    if train_type == 'surface':
        tr_dataset = DataLoader_Surface(annot_file, 'train')
        te_dataset = DataLoader_Surface(annot_file, 'test')
    elif train_type == 'point':
        tr_dataset = DataLoader_Point(annot_file, 'train')
        te_dataset = DataLoader_Point(annot_file, 'test')
    else:
        raise ValueError('Data loader type ' + train_type + ' not recognized.')
    return tr_dataset, te_dataset
