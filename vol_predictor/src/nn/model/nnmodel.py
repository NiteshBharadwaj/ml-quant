import torch.nn as nn


class Linear(nn.Module):
    def __init__(self, inp_size, opt_size, hidden_size=1024, hidden_size2=64):
        super(Linear, self).__init__()
        self.regressor = nn.Sequential(nn.Linear(inp_size, hidden_size),
                                       nn.BatchNorm1d(hidden_size),
                                       nn.Dropout(),
                                       nn.Linear(hidden_size, hidden_size),
                                       nn.BatchNorm1d(hidden_size),
                                       nn.Dropout(),
                                       nn.Linear(hidden_size, hidden_size2),
                                       nn.BatchNorm1d(hidden_size2),
                                       nn.Linear(hidden_size2, opt_size))

    def forward(self, inp):
        return self.regressor(inp)
