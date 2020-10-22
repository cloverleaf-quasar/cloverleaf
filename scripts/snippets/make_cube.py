import numpy as np
from astropy.io import fits


imgfits = ['/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-100km_s_1src/sie_es_-100km_s_image.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-50km_s_1src/sie_es_-50km_s_image.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_0km_s_1src/sie_es_0km_s_image.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_50km_s_1src/sie_es_50km_s_image.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_100km_s_1src/sie_es_100km_s_image.fits']
srcfits = ['/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-100km_s_1src/sie_es_-100km_s_source.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-50km_s_1src/sie_es_-50km_s_source.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_0km_s_1src/sie_es_0km_s_source.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_50km_s_1src/sie_es_50km_s_source.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_100km_s_1src/sie_es_100km_s_source.fits']
resfits = ['/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-100km_s_1src/sie_es_-100km_s_residual.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_-50km_s_1src/sie_es_-50km_s_residual.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_0km_s_1src/sie_es_0km_s_residual.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_50km_s_1src/sie_es_50km_s_residual.fits',
            '/Users/Tsuyoshi/Documents/cloverleaf/result/siees_100km_s_1src/sie_es_100km_s_residual.fits']            

imgdata, imgheader = fits.getdata(imgfits[0], header=True)
srcdata, srcheader = fits.getdata(srcfits[0], header=True)
resdata, resheader = fits.getdata(resfits[0], header=True)

imgcube = np.zeros([len(imgfits), imgdata.shape[1], imgdata.shape[0]])
srccube = np.zeros([len(srcfits), srcdata.shape[1], srcdata.shape[0]])
rescube = np.zeros([len(resfits), resdata.shape[1], resdata.shape[0]])

imgname = 'modeled_image.fits'
srcname = 'modeled_source.fits'
resname = 'residual.fits'

for i, fitsdata in enumerate(zip(imgfits, srcfits, resfits)):
    imgcube[i] += fits.getdata(fitsdata[0])
    srccube[i] += fits.getdata(fitsdata[1])
    rescube[i] += fits.getdata(fitsdata[2])

fits.writeto(imgname, imgcube, overwrite=True)
fits.writeto(srcname, srccube, overwrite=True)
fits.writeto(resname, rescube, overwrite=True)