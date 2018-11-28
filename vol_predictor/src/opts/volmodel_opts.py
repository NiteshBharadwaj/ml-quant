import argparse
import os
import opts.ref
from opts.opts import Opts


class VolModelOpts(Opts):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()
        self.parser.add_argument('-volModel', default='black_cubic', help='Vol Model')
        self.parser.add_argument('-nRows', default=30000, type=int, help='Size of data')
        self.parser.add_argument('-gridSize', default=100, type=int, help='Size of data')
        self.parser.add_argument('-strikePerturb', default=0.0, type=float, help='Strike perturbation for data augment')
        self.parser.add_argument('-matPerturb', default=0.0, type=float, help='Maturity perturbation for data augment')
        self.parser.add_argument('-volPerturb', default=0.05, type=float, help='Volatility perturbation for data augment')