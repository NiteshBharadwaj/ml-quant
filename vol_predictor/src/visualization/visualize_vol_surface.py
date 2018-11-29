import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os


# Inspired from: http://gouthamanbalaraman.com/blog/volatility-smile-heston-model-calibration-quantlib-python.html

def visualize_vol_surface_helper(X, Y, Z, name=None, saveDir=None, xlabel='Strikes', ylabel='Maturity(years)', zlabel='Volatility'):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.set_zlabel(zlabel)
    if not name is None:
        plt.title(name)
        fname = os.path.join(saveDir, name + '.pdf')
        plt.savefig(fname)
    plt.show(block=True)


def visualize_vol_surface(surface, strike_min, strike_max, t_min, t_max, name=None, saveDir=None):
    plot_years = np.arange(t_min, t_max, 0.1)
    plot_strikes = np.arange(strike_min, strike_max, 1)
    X, Y = np.meshgrid(plot_strikes, plot_years)
    Z = np.array([surface.get_vol(x, y)
                  for xr, yr in zip(X, Y)
                  for x, y in zip(xr, yr)]
                 ).reshape(len(X), len(X[0]))
    visualize_vol_surface_helper(X, Y, Z, name, saveDir)


def visualize_vol_surface2(surface, plot_strikes, plot_years, name=None, saveDir=None):
    X, Y = np.meshgrid(plot_strikes, plot_years)
    Z = surface.transpose()
    visualize_vol_surface_helper(X, Y, Z, name, saveDir, xlabel='Moneyness')

def visualize_vol_surface_overlap(surf1, surf2, strike_low, strike_high, start_time,
                                  end_time, nStrikes, nMats, saveDir=None):
    time_step = (end_time - start_time) / nMats
    strike_step = (strike_high - strike_low) / nStrikes
    plot_years = np.arange(start_time, end_time, time_step)
    plot_strikes = np.arange(strike_low, strike_high, strike_step)
    visualize_vol_surface2(surf1, plot_strikes, plot_years, 'surface_nn_output', saveDir)
    visualize_vol_surface2(surf2, plot_strikes, plot_years, 'surface_gt', saveDir)
    visualize_vol_surface2(surf1 - surf2, plot_strikes, plot_years, 'diff', saveDir)
