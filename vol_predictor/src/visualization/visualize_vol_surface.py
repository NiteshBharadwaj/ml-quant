import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
# Inspired from: http://gouthamanbalaraman.com/blog/volatility-smile-heston-model-calibration-quantlib-python.html

def visualize_vol_surface(surface, strike_min, strike_max, t_min, t_max, name = None, saveDir = None):
    plot_years = np.arange(t_min, t_max, 0.1)
    plot_strikes = np.arange(strike_min, strike_max, 1)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(plot_strikes, plot_years)
    Z = np.array([surface.get_vol(x, y)
                  for xr, yr in zip(X, Y)
                  for x, y in zip(xr, yr)]
                 ).reshape(len(X), len(X[0]))

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.xlabel('Strikes')
    plt.ylabel('Maturity (years)')
    ax.set_zlabel('Volatility')
    if not name is None:
        plt.title(name+'_vol_surface')
        fname = os.path.join(saveDir,name+'.pdf')
        plt.savefig(fname)
    plt.show(block = True)