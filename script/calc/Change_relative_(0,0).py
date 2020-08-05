#!/usr/bin/env python
# coding: utf-8

# ### fitsの(0,0)を検出(template)

# In[9]:


import astropy.io.fits as iofits
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.coordinates import Angle

#### 観測fits名前 ########################
# Cloverleaf_CO_3-2_rob+0.0_mom0.fits
# Cloverleaf_rob0_CO_3-2_mom0_-500to500.fits
#####################################

#### fitsの読み込み ####
fits = input("fits name:")
list = iofits.open(fits)

#### リストの選択 ####
pic = list[0]
header = pic.header
data = pic.data

#### header情報の取得 ####
#OBSRA   =   2.139427083333E+02  deg                                             
#OBSDEC  =   1.149538888889E+01 deg
obsra = header['OBSRA']
obsdec = header['OBSDEC']

## deg表示 ##
obsra_deg = Angle(obsra * u.deg)
obsdec_deg = Angle(obsdec * u.deg)

## arcsec 表示 ##
obsra_arcsec = obsra_deg.arcsec
obsdec_arcsec = obsdec_deg.arcsec

print(str(fits)+'の'+'R.A.:',obsra_deg.deg,'deg')
print(str(fits)+'の'+'Decl.:',obsdec_deg.deg,'deg')
print(str(fits)+'の'+'R.A.:',obsra_arcsec,'arcsec')
print(str(fits)+'の'+'Decl.:',obsdec_arcsec,'arcsec')

#print(str(fits)+'の'+'R.A.:',obsra_arcsec,'arcsec')
#print(str(fits)+'の'+'Decl.:',obsdec_arcsec,'arcsec')
## 通常表示 ##
#print(str(fits)+'の'+'R.A.:',obsra_deg,'deg')
#print(str(fits)+'の'+'Decl.:',obsdec_deg,'deg') 


# ### 合わせたい相対座標の(0,0)を入力

# In[13]:


#### 変換 ####

#### example ####
## Venturini 2003 
# R.A. 14h15m46.233s
# Decl. 11d29'43.50"

## Akhunov 2017 
# R.A. 14h15m46.222s
# Decl. 11d29'43.015"

# R.A.

ra = Angle(input('R.A.を入力( # Hour, minute, second )'))
RA_result = ra.degree
           
# Decl.
dec = Angle(input('Decl.を入力(# Degree, arcmin, arcsec )'))
Decl_result = dec.degree
 
#### 表示 ####
print('R.A.:',ra.degree,'deg',',',ra.arcsec,'arcsec')
print('Decl.:',dec.degree,'deg',',',dec.arcsec,'arcsec')


# ### 両者の中心(0,0)の差を計算する(例 template(glafic)-Akhunov)

# In[14]:


#### data ####

# 観測fitsの中心座標
## R.A. (arcsec)
## obsra_arcsec

## Decl. (arcsec)
## obsdec_arcsec

# 合わせたい論文の中心座標
## R.A. (arcsec)
## ra.arcsec

## Decl. (arcsec)
## dec.arcsec

#### 実行 #### 
RA_sa_sekidou = obsra_arcsec - ra.arcsec
Decl_sa = obsdec_arcsec - dec.arcsec

print('R.A.方向の差(赤道上での):',RA_sa_sekidou,'arcsec')
print('Decl.方向の差:',Decl_sa,'arcsec')


# ### 赤道上でのR.A.方向の差を緯度分補正する

# In[15]:


#### 緯度の入力 ####
#ido_deg = Angle(float(input('緯度(deg):')), u.degree) # 緯度を自分で入力
ido_deg = obsdec_deg
ido = ido_deg.radian
#print(ido)

#### example ####
#RA_sa_sekidou = 90

#### 補正 ####
RA_sa = RA_sa_sekidou * np.cos(ido)

#print(np.cos(ido))
print('赤道上でのRA方向の差:',RA_sa_sekidou,'arcsec')
print('template(glafic)平面上でのRA方向の差:',RA_sa,'arcsec')
#print(np.cos(ido))


# ### 論文座標をtemplate座標に変換

# In[19]:


#### 差 ####
#print('差',RA_sa,'arcsec')
#print('差',Decl_sa,'arcsec')

#### example ####
#best fit G1(200 km/s)
## Δα = -0.1712028 (arcsec)
## Δδ = 0.2523334 (arcsec)

#best fit G1(500 km/s)
## Δα = -0.169 (arcsec)
## Δδ = 0.216 (arcsec)

#Akhunov 2017 G1
## Δα = -0.163 (arcsec)
## Δδ = 0.550 (arcsec)

para_ra = float(input('glafic座標に変換したいR.A.を代入(arcsec):'))
para_dec = float(input('glafic座標に変換したいDecl.を代入(arcsec):'))

#### 計算 ####
kotae_ra = RA_sa + para_ra
kotae_dec = Decl_sa + para_dec

#### 表示 ####
print('変換後座標(R.A.):',kotae_ra,'arcsec')
print('変換後座標(Decl.):',kotae_dec,'arcsec')

