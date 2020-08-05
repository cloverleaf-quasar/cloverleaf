import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# from astropy.wcs import WCS

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
    
    ax[0].axis('off')
    ax[0].set_title('obs')
    mappable0 = ax[0].imshow(imgfits, origin='lower', cmap='jet')
    divider0  = make_axes_locatable(ax[0])
    cax0      = divider0.append_axes('bottom', size='5%', pad=0.05)
    fig.colorbar(mappable0, cax=cax0, orientation='horizontal')

    ax[1].axis('off')
    ax[1].set_title('mod')
    mappable1 = ax[1].imshow(fitsfile, origin='lower', cmap='jet')
    divider1  = make_axes_locatable(ax[1])
    cax1      = divider1.append_axes('bottom', size='5%', pad=0.05)
    fig.colorbar(mappable1, cax=cax1, orientation='horizontal')

    ax[2].axis('off')
    ax[2].set_title('res')
    mappable2 = ax[2].imshow(resfits, origin='lower', cmap='jet')
    divider2  = make_axes_locatable(ax[2])
    cax2      = divider2.append_axes('bottom', size='5%', pad=0.05)
    fig.colorbar(mappable2, cax=cax2, orientation='horizontal')

    fig.tight_layout()
    fig.savefig(imgout)
    fig.show()