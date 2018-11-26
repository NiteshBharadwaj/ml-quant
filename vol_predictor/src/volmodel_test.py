from .data_process.parse_vol_data import parse_vol_data
def cubic_spline_test(opt):
    data = opt.dataDir
    data_parsed = parse_vol_data(data)
