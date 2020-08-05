#!/usr/bin/env python
# coding: utf-8

# ### 共動距離(D_ls導出のため)

# In[1]:


from astropy.constants import pc
### 共同距離は、単純な足し算が可能
# lens : D_com = 5236.3 Mpc
# source : D_com = 6038.9 Mpc
# D_ls : D_source - D_lens

### パーセク
# lens
#D_com_lens = 5.2363e+9 
D_com_lens = float(input('lensの共動距離(Mpc)(http://www.astro.ucla.edu/):')) * 1.0e+6

# source
#D_com_source = 6.0389e+9
D_com_source = float(input('sourceの共動距離(Mpc)(http://www.astro.ucla.edu/):')) * 1.0e+6

#### 共動距離lsの計算 ####
D_com_ls = D_com_source - D_com_lens
print('D_com_ls:',D_com_ls)

#### D_ls 角径距離 ####
D_ls = pc * D_com_ls
print('D_ls:',D_ls)


# ### 角径距離

# In[2]:


from astropy.constants import pc

#### lens ####
# 1775 Mpc
#lens_kaku = pc * 1.775e+9
D_lens = pc * float(input('lensの角形距離(Mpc)(http://www.astro.ucla.edu/)：')) * 1.0e+6
print('lens:',D_lens)

#### source ####
# 1697.4 Mpc 
#source_kaku = pc * 1.6974e+9
D_source = pc * float(input('sourceの角形距離(Mpc)(http://www.astro.ucla.edu/)：')) *1.0e+6
print('source:',D_source)


# ### Einstein radius

# In[10]:


import numpy as np
from astropy import units as u
from astropy.coordinates import Angle

#### Einstein radiousのinput ####
# arcsec → rad
arcsec = Angle(float(input('Einstein radious(arcsec)を入力:')),u.arcsec)
rad = arcsec.radian

print('Einstein radius(radian)',rad,'rad')


# ### 計算

# In[11]:


from astropy.constants import c
from astropy.constants import G
### メモ
# rad : Einstein radius(radian)
# M :　質量(kg)

### 計算 ###
M_0 = rad**2 
print('M_0',M_0)

M_1 = c**2 
print('M_1:',M_1)

M_2 = D_lens * D_source
print('M_2:',M_2)

M_3 = (4*G)**-1
print('M_3:',M_3)

M_4 = (D_ls)**-1
print('M_4:',M_4)

M = M_0*M_1*M_2*M_3*M_4
print('M=',M)


# ### kg→太陽質量

# In[5]:


from astropy.constants import M_sun
M_taiyou = M / M_sun

print('太陽質量表示','{:E}'.format(M_taiyou),)

