import numpy as np


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