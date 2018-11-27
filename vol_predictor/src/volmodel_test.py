from data_process.parse_vol_data import parse_vol_data
from vol_models.black_cubic import BlackCubic
from vol_models.dupire_local import DupireLocal
from vol_models.heston_slv import HestonSLV
from visualization.visualize_vol_surface import visualize_vol_surface
from opts.volmodel_opts import VolModelOpts


def black_cubic_test(opt):
    data = opt.data
    data_parsed = parse_vol_data(data)
    vol_model = BlackCubic(data_parsed[0])
    visualize_vol_surface(vol_model, 535.0, 730.0, 0.0, 2.0, name = 'black_cubic', saveDir = opt.saveDir)


def dupire_local_test(opt):
    data = opt.data
    data_parsed = parse_vol_data(data)
    vol_model = DupireLocal(data_parsed[0])
    visualize_vol_surface(vol_model, 535.0, 730.0, 0.0, 2.0, name = 'dupire_local', saveDir = opt.saveDir)


def heston_slv_test(opt):
    data = opt.data
    data_parsed = parse_vol_data(data)
    vol_model = HestonSLV(data_parsed[0])
    visualize_vol_surface(vol_model, 535.0, 730.0, 0.0, 2.0, name = 'heston_slv', saveDir = opt.saveDir)


def main():
    opt = VolModelOpts().parse()
    print('Black cubic vol surface:')
    black_cubic_test(opt)
    print('Dupire local vol surface:')
    dupire_local_test(opt)
    print('Heston stochastic local vol surface:')
    heston_slv_test(opt)


if __name__ == '__main__':
    main()