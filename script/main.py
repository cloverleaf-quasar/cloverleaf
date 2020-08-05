##### dependencies #####
import pathlib, shutil
import numpy as np
import yaml
from astropy import units as u
from astropy.io import fits
from subprocess import Popen, PIPE
from misc.makeinput import makeinput


##### load yaml #####
cur_dir        = pathlib.Path.cwd()
cloverleaf_dir = pathlib.Path(__file__).parents[1].resolve()
data_dir       = cloverleaf_dir / pathlib.Path('data')
input_dir      = cloverleaf_dir / pathlib.Path('input')
result_dir     = cloverleaf_dir / pathlib.Path('result')

config_file = cloverleaf_dir / pathlib.Path('script/config/glafic.yaml')
with open(config_file) as file:
    yml = yaml.load(file)

##### filenames #####
input_b   = input_dir / pathlib.Path(yml['filename']['input_b'])
input_a   = input_dir / pathlib.Path(yml['filename']['input_a'])
input_as  = input_dir / pathlib.Path(yml['filename']['input_as'])
fitsfile  = data_dir / pathlib.Path(yml['filename']['obsfits'])
noisefile = data_dir / pathlib.Path(yml['filename']['noisefits'])
psffile   = data_dir / pathlib.Path(yml['filename']['psffits'])
if yml['user_params']['mask'] is True:
    maskfile = data_dir / pathlib.Path(yml['filename']['maskfits'])
else:
    maskfile = ''
optfile   = result_dir / pathlib.Path(yml['filename']['optfile'])
imgfits   = result_dir / pathlib.Path(yml['filename']['imgfits'])
srcfits   = result_dir / pathlib.Path(yml['filename']['srcfits'])
resfits   = result_dir / pathlib.Path(yml['filename']['resfits'])

glafic_path = pathlib.Path(yml['path']['glafic'])

##### basic source information #####
zs        = yml['user_params']['zs']
pix_ext_s = yml['user_params']['pix_ext_s']

## input info
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
makeinput(input_b, primary_params, secondary_params, lens_models, source_models, lens_opt, source_opt)

### optimization ###
proc = Popen([glafic_path, input_b], stdin=PIPE)
proc.communicate('readobs_extend {} {}\nreadnoise_extend {}\nreadpsf {}\noptimize\nquit\n'.format(fitsfile, maskfile, noisefile, psffile).encode())
shutil.move(cur_dir / optfile.name, optfile)

### read fitting results ###
with open(optfile, 'r') as fp_opt:
    optdata         = fp_opt.readlines()
    lens_models_a   = optdata[-source_num-lens_num-1:-source_num-1]
    source_models_a = optdata[-source_num-1:-1]

### make input_a ###
makeinput(input_a, primary_params, secondary_params, lens_models_a, source_models_a, lens_opt, source_opt)

### calculate modeled image ###
proc = Popen([glafic_path, input_a], stdin=PIPE)
proc.communicate('writeimage 0 0\nquit\n'.encode())
shutil.move(cur_dir / imgfits.name, imgfits)

### make input_as ###
primary_params['pix_ext'] = pix_ext_s
makeinput(input_as, primary_params, secondary_params, lens_models_a, source_models_a, lens_opt, source_opt)

### output the source plane ###
proc = Popen([glafic_path, input_as], stdin=PIPE)
proc.communicate('writeimage_ori 0 0\nquit\n'.encode())
shutil.move(cur_dir / srcfits.name, srcfits)

### make residual image
data, header   = fits.getdata(imgfits, header=True)
rdata, rheader = fits.getdata(fitsfile, header=True)
if source_num > 1:
    fits.writeto(resfits, rdata-data[-1], rheader, overwrite=True)
else:
    fits.writeto(resfits, rdata-data, rheader, overwrite=True)