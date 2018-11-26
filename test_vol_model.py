from vol_predictor.src.volmodel_opts import volmodel_opts as opts
from vol_predictor.src.volmodel_test import cubic_spline_test, dupire_test

def main():
    opt = opts().parse()
    cubic_spline_test(opt)
    dupire_test(opt)

if __name__ == 'main':
    main()




