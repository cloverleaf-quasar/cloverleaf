##### dependencies #####
from itertools import product
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mc
plt.style.use('seaborn-pastel')
plt.rcParams['font.size'] = 5
from matplotlib.gridspec import GridSpec

##### data reduction #####
data = pd.read_csv('sie_es_mcmc.dat', delim_whitespace=True, header=None)
data.drop(6, axis=1, inplace=True)
data.drop(7, axis=1, inplace=True)
data.rename(columns={8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 11, 14: 12, 15: 13, 16: 14}, inplace=True)

# data[5] -= np.floor(data[5] / 180) * 180
# data[7] -= np.floor(data[7] / 180) * 180

##### user-defined parameters #####
burn_in = 0.2
labels1 = [r'$P(\sigma)$', r'$P(x_\mathrm{c})$', r'$P(y_\mathrm{c})$',
           r'$P(e)$', r'$P(\theta_e)$', r'$P(\gamma)$', r'$P(\theta_\gamma)$']
labels2 = [r'$\sigma$ [km/s]', r'$x_\mathrm{c}$ [arcsec]',
           r'$y_\mathrm{c}$ [arcsec]', r'$e$', r'$\theta_e$ [deg]',
           r'$\gamma$', r'$\theta_\gamma$ [deg]']
labels3 = [r'$P(F)$', r'$P(x_\mathrm{c})$', r'$P(y_\mathrm{c})$', r'$P(e)$', r'$P(\theta_e)$', r'$P(\sigma)$']
labels4 = [r'flux', r'$x_\mathrm{c}$ [arcsec]', r'$y_\mathrm{c}$ [arcsec]', r'$e$', r'$\theta_e$ [deg]', r'$\sigma$ [arcsec]']

num     = 7 # the number of lens parameters
num_s   = 6 # the number of source parameters
num_ss  = 1 # the number of sources

##### main #####
fig = plt.figure()
gs  = GridSpec(num, num)
for i, j in product(range(num), range(num)):
    if j < i:
        continue
    ax = fig.add_subplot(gs[j, i])

    if i == j:
        if i != num - 1:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(labels2[j])
            pass
        ax.set_yticks([])
        ax.set_yticklabels([])

        hist, bins = np.histogram(data[i+1][int(len(data)*burn_in):],
                                  bins=50)
        max_val    = max(hist)
        hist       = [float(n) / max_val for n in hist]
        center     = (bins[:-1] + bins[1:]) / 2
        width      = 0.7 * (bins[1] - bins[0])

        ax2 = ax.twinx()
        ax2.bar(center, hist, align='center', width=width)
        ax2.set_ylabel(labels1[i])
    else:
        counts, xedges, yedges, Image = ax.hist2d(data[i+1][int(len(data)*burn_in):],
                                                  data[j+1][int(len(data)*burn_in):],
                                                  bins=[50, 50], norm=mc.LogNorm())
        ax.contour(counts.transpose(), extent=[xedges.min(), xedges.max(), yedges.min(), yedges.max()], linewidth=5)
        if i == 0:
            ax.set_ylabel(labels2[j])
            if j != num - 1:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(labels2[i])
                pass
        elif j == num - 1:
            ax.set_xlabel(labels2[i])
            ax.set_yticklabels([])
        else:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
fig.subplots_adjust(wspace=0.1, hspace=0.1)
fig.savefig('mcmc_result.pdf')
fig.show()

for k in range(num_ss):
    fig = plt.figure()
    gs  = GridSpec(num_s, num_s)
    for i, j in product(range(num_s), range(num_s)):
        if j < i:
            continue
        ax = fig.add_subplot(gs[j, i])

        if i == j:
            if i != num_s - 1:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(labels4[j])
                pass
            ax.set_yticks([])
            ax.set_yticklabels([])

            hist, bins = np.histogram(data[num+(i+1)+num_s*k][int(len(data)*burn_in):],
                                      bins=50)
            max_val    = max(hist)
            hist       = [float(n) / max_val for n in hist]
            center     = (bins[:-1] + bins[1:]) / 2
            width      = 0.7 * (bins[1] - bins[0])

            ax2 = ax.twinx()
            ax2.bar(center, hist, align='center', width=width)
            ax2.set_ylabel(labels3[i])
        else:
            counts, xedges, yedges, Image = ax.hist2d(data[num+(i+1)+num_s*k][int(len(data)*burn_in):],
                                                      data[num+(j+1)+num_s*k][int(len(data)*burn_in):],
                                                      bins=[50, 50], norm=mc.LogNorm())
            ax.contour(counts.transpose(), extent=[xedges.min(), xedges.max(), yedges.min(), yedges.max()], linewidth=5)
            if i == 0:
                ax.set_ylabel(labels3[j])
                if j != num_s - 1:
                    ax.set_xticklabels([])
                else:
                    ax.set_xlabel(labels4[i])
                    pass
            elif j == num_s - 1:
                ax.set_xlabel(labels4[i])
                ax.set_yticklabels([])
            else:
                ax.set_xticklabels([])
                ax.set_yticklabels([])
    fig.subplots_adjust(wspace=0.1, hspace=0.1)
    fig.savefig('mcmc_result_{}.pdf'.format(k+1))
    fig.show()
