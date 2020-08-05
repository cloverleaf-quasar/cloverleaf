##### dependencies #####
import sys
import pathlib, shutil
import numpy as np
import yaml
import datetime
from astropy import units as u
from astropy.io import fits
from subprocess import Popen, PIPE
# from subprocess import run as srun
from misc.makeinput import makeinput


##### get current time #####
now     = datetime.datetime.now()
dirname = now.strftime('%Y%m%d_%H%M%S')

##### get arguments #####
argv = sys.argv
argc = len(argv)
if argc != 2:
    raise SyntaxError('The number of arguments is wrong!')
ymlname = argv[1]

##### directory setting #####
cur_dir        = pathlib.Path.cwd()
cloverleaf_dir = pathlib.Path(__file__).parents[1].resolve()
data_dir       = cloverleaf_dir / 'data'
input_dir      = cloverleaf_dir / 'input' / dirname
result_dir     = cloverleaf_dir / 'result' / dirname

input_dir.mkdir()
result_dir.mkdir()

# config_file = cloverleaf_dir / pathlib.Path('script/config/glafic_source2.yaml')
with open(ymlname) as file:
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
# srun([glafic_path, input_b])
proc.communicate('readobs_extend {} {}\nreadnoise_extend {}\nreadpsf {}\noptimize\nquit\n'.format(fitsfile, maskfile, noisefile, psffile).encode())
# proc.stdin.write('readobs_extend {} {}\n'.format(fitsfile, maskfile).encode())
# proc.stdin.flush()
# proc.stdin.write('readnoise_extend {}\n'.format(noisefile).encode())
# proc.stdin.flush()
# proc.stdin.write('readpsf {}\n'.format(psffile).encode())
# proc.stdin.flush()
# proc.stdin.write('optimize\n'.encode())
# proc.stdin.flush()
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
proc.communicate('readpsf {}\nwriteimage 0 0\nquit\n'.format(psffile).encode())
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