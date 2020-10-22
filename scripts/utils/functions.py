import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def makeinput(filename, primary_params, secondary_params, lens_models, source_models, lens_opt, source_opt):
    fp = open(filename, 'w')

    fp.write('### primary parameters ###\n')
    for key, value in primary_params.items():
        fp.write('{}\t{}\n'.format(key, value))
    fp.write('\n')

    fp.write('### secondary parameters ###\n')
    for key, value in secondary_params.items():
        fp.write('{}\t{}\n'.format(key, value))
    fp.write('\n')

    fp.write('### startup ###\n')
    fp.write('startup {} {} 0\n'.format(len(lens_models), len(source_models)))
    fp.write('### lens model ###\n')
    np.savetxt(fp, lens_models, fmt='%s')
    fp.write('### extended source model ###\n')
    np.savetxt(fp, source_models, fmt='%s')
    fp.write('end_startup\n')
    fp.write('\n')

    fp.write('### optimization ###\n')
    fp.write('start_setopt\n')
    fp.write('### lens opt ###\n')
    np.savetxt(fp, lens_opt, fmt='%s')
    fp.write('### extended source opt ###\n')
    np.savetxt(fp, source_opt, fmt='%s')
    fp.write('end_setopt\n')
    fp.write('\n')

    fp.write('### execute commands\n')
    fp.write('start_command\n')
    fp.write('\n')

    fp.close()

def makefigure(imgout, imgfits, fitsfile, resfits):
    fig, ax = plt.subplots(1, 3, figsize=(10, 4))

    title = ['obs', 'mod', 'res']
    data  = [imgfits, fitsfile, resfits]
    for ax_, title_, data_ in zip(ax, title, data):
        ax_.axis('off')
        ax_.set_title(title_)
        mappable = ax_.imshow(data_, origin='lower', cmap='jet')
        divider  = make_axes_locatable(ax_)
        cax      = divider.append_axes('bottom', size='5%', pad=0.05)
        fig.colorbar(mappable, cax=cax, orientation='horizontal')

    fig.tight_layout()
    fig.savefig(imgout)
    fig.show()

def makestats(statout, statdict, show=True):
    ### to be updated
    with open(statout, 'w') as fp:
        for key, value in statdict.items():
            fp.write(f'{key}\t{value}\n')

    if show:
        print('')
        print('summary')
        print('===================================')
        print('elapsed time = {:.1e} [sec]'.format(statdict['elapsed_time']))
        print('')
        print('chi^2 = {:.1e}'.format(statdict['chi^2']))
        print('Ndata = {}'.format(statdict['Ndata']))
        print('reduced chi^2 = {:.1f}'.format(statdict['reduced_chi^2']))
        print('')
        print('obs min/max = {:.2e} / {:.2e}'.format(statdict['obs_min'], statdict['obs_max']))
        print('mod min/max = {:.2e} / {:.2e}'.format(statdict['mod_min'], statdict['mod_max']))
        print('res min/max = {:.2e} / {:.2e}'.format(statdict['res_min'], statdict['res_max']))
        print('===================================')