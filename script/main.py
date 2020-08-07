##### dependencies #####
import sys
import pathlib, shutil
import numpy as np
import yaml
import time, datetime
from astropy import units as u
from astropy.io import fits
from subprocess import Popen, PIPE
from misc import functions as f


##### get current time #####
now   = datetime.datetime.now()
start = time.time()
anaid = now.strftime('%Y%m%d_%H%M%S')

##### get arguments #####
argv = sys.argv
argc = len(argv)
if argc != 2 and argc != 3:
    raise SyntaxError('The number of arguments is wrong!')
if '-qlook' in argv:
    qlook = True
    argv.remove('-qlook')
else:
    qlook = False
ymlname = argv[-1]

##### directory setting #####
cur_dir        = pathlib.Path.cwd()
cloverleaf_dir = pathlib.Path(__file__).parents[1].resolve()
data_dir       = cloverleaf_dir / 'data'
input_dir      = cloverleaf_dir / 'input' / anaid
result_dir     = cloverleaf_dir / 'result' / anaid

input_dir.mkdir()
result_dir.mkdir()

with open(ymlname) as file:
    yml = yaml.load(file)
shutil.copy(ymlname, input_dir)

##### filenames #####
prefix    = yml['primary_params']['prefix']
fitsfile  = data_dir / pathlib.Path(yml['filename']['obsfits'])
noisefile = data_dir / pathlib.Path(yml['filename']['noisefits'])
psffile   = data_dir / pathlib.Path(yml['filename']['psffits'])

mask  = yml['user_params']['mask']
prior = yml['user_params']['prior']
mcmc  = yml['user_params']['mcmc']
if mask:
    maskfile = data_dir / pathlib.Path(yml['filename']['maskfits'])
    shutil.copy(maskfile, input_dir)
else:
    maskfile = ''
if prior:
    priorfile = data_dir / pathlib.Path(yml['filename']['priorfile'])
    shutil.copy(priorfile, input_dir)
else:
    priorfile = ''

input_b   = input_dir / pathlib.Path(prefix + yml['filename']['input_b'])
input_a   = input_dir / pathlib.Path(prefix + yml['filename']['input_a'])
input_as  = input_dir / pathlib.Path(prefix + yml['filename']['input_as'])
optfile   = result_dir / pathlib.Path(prefix + yml['filename']['optfile'])
imgfits   = result_dir / pathlib.Path(prefix + yml['filename']['imgfits'])
srcfits   = result_dir / pathlib.Path(prefix + yml['filename']['srcfits'])
resfits   = result_dir / pathlib.Path(prefix + yml['filename']['resfits'])
imgout    = result_dir/ pathlib.Path(yml['filename']['imgout'])
statout   = result_dir/ pathlib.Path(yml['filename']['statout'])

glafic_path = pathlib.Path(yml['path']['glafic'])

##### basic source information #####
zs        = yml['user_params']['zs']
pix_ext_s = yml['user_params']['pix_ext_s']

##### model info #####
primary_params   = yml['primary_params']
secondary_params = yml['secondary_params']
lens_models      = yml['model']['lens'].split('\n')
source_models    = yml['model']['source'].split('\n')
lens_num         = len(lens_models)
source_num       = len(source_models)
lens_opt         = yml['optimization']['lens'].split('\n')
source_opt       = yml['optimization']['source'].split('\n')

##### main #####
### make input_b ###
f.makeinput(input_b, primary_params, secondary_params, lens_models, source_models, lens_opt, source_opt)

### optimization ###
proc = Popen([glafic_path, input_b], stdin=PIPE)
proc.communicate('readobs_extend {} {}\nreadnoise_extend {}\nreadpsf {}\nparprior {}\noptimize\nquit\n'\
                .format(fitsfile, maskfile, noisefile, psffile, priorfile).encode())
shutil.move(cur_dir / optfile.name, optfile)

### read fitting results ###
with open(optfile, 'r') as fp_opt:
    optdata         = fp_opt.readlines()
    lens_models_a   = optdata[-source_num-lens_num-1:-source_num-1]
    source_models_a = optdata[-source_num-1:-1]

    statdata = optdata[-source_num-lens_num-1-8].split()
    chi2     = float(statdata[2])
    ndata    = int(statdata[-1].rstrip(']'))

### make input_a ###
f.makeinput(input_a, primary_params, secondary_params, lens_models_a, source_models_a, lens_opt, source_opt)

### calculate modeled image ###
proc = Popen([glafic_path, input_a], stdin=PIPE)
proc.communicate('readpsf {}\nwriteimage 0 0\nquit\n'.format(psffile).encode())
shutil.move(cur_dir / imgfits.name, imgfits)

### mcmc ###
if mcmc:
    mcmcfile  = result_dir / pathlib.Path(prefix + yml['filename']['mcmcfile'])
    sigmafile = data_dir / pathlib.Path(yml['filename']['sigmafile'])
    mcmc_n    = yml['user_params']['mcmc_n']
    shutil.copy(sigmafile, input_dir)

    proc = Popen([glafic_path, input_a], stdin=PIPE)
    proc.communicate('readobs_extend {} {}\nreadnoise_extend {}\nreadpsf{}\nparprior {}\nmcmc_sigma {}\nmcmc {} extend\nquit\n'\
                    .format(fitsfile, maskfile, noisefile, psffile, priorfile, sigmafile, mcmc_n).encode())
    shutil.move(cur_dir / mcmcfile.name, mcmcfile)

### make input_as ###
primary_params['pix_ext'] = pix_ext_s
f.makeinput(input_as, primary_params, secondary_params, lens_models_a, source_models_a, lens_opt, source_opt)

### output the source plane ###
proc = Popen([glafic_path, input_as], stdin=PIPE)
proc.communicate('writeimage_ori 0 0\nquit\n'.encode())
shutil.move(cur_dir / srcfits.name, srcfits)

### make residual image
data, header   = fits.getdata(imgfits, header=True)
rdata, rheader = fits.getdata(fitsfile, header=True)
if source_num > 1:
    data    = data[-1]
    resdata = rdata - data
else:
    resdata = rdata - data
fits.writeto(resfits, resdata, rheader, overwrite=True)

### make combined image ###
f.makefigure(imgout, rdata, data, resdata)

### make statistics ###
elapsed_time = time.time() - start
statdict = {'elapsed_time': elapsed_time, 'chi^2': chi2, 'Ndata': ndata, 'reduced_chi^2': chi2 / ndata,
            'obs_max': rdata.max(), 'obs_min': rdata.min(),
            'mod_max': data.max(), 'mod_min': data.min(),
            'res_max': resdata.max(), 'res_min': resdata.min()}
f.makestats(statout, statdict)

### qlook ###
if qlook:
    shutil.rmtree(input_dir)
    shutil.rmtree(result_dir)