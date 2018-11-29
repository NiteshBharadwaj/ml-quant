from opts.opts import Opts


class NNModelOpts(Opts):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()
        self.parser.add_argument('-volModel', default='black_cubic', help='Vol Model')
        self.parser.add_argument('-nnModel', default='linear', help='NN Model')
        self.parser.add_argument('-trainType', default='surface', help='Train type')
        self.parser.add_argument('-LR', type=float, default=1e-3, help='Learn rate')
        self.parser.add_argument('-dropLR', type=float, default=10, help='Drop LR')
        self.parser.add_argument('-nEpochs', type=int, default=25, help='Epochs')
        self.parser.add_argument('-valInterval', type=int, default=5, help='Val Interval')
        self.parser.add_argument('-batchSize', type=int, default=64, help='Batch Size')
        self.parser.add_argument('-loadModel', default='none', help='Load pre-trained')
        self.parser.add_argument('-train', dest='train',  action='store_true', help='Train')