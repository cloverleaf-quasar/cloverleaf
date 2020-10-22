#!/usr/bin/env python
# coding: utf-8

# ### 質量(kg)→速度分散(m/s)

# In[22]:


#### ライブラリーのimport ####

from astropy.constants import pc
from astropy import units as u
from astropy.coordinates import Angle
import numpy as np
from astropy.constants import c
from astropy.constants import G
from astropy.constants import M_sun

#### 定義 ####

D_s =  5.477077707104265e+25
D_d =  5.2376291267824115e+25
D_ds = 2.477490530160008e+25

M = float(input('質量(kg):'))

#### 式 ####

def sigma_v(M):
    return ((c**2 * G * M * D_s)/(4* (np.pi)**2 * D_d * D_ds))**(1/4)

#### 速度分散 ####

## m/s ##
print(sigma_v(M),'m/s')
sigma_v_km = sigma_v(M)/1000

## km/s ##
print('速度分散σ:',sigma_v_km,'km/s')

