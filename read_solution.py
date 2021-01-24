#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 12:02:19 2021

@author: Geoffroy Lesur (geoffroy.lesur@univ-grenoble-alpes.fr)
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import sys

# Check if a filename has been fiven on command line
if len(sys.argv)>1:
    filename = str(sys.argv[1])
else:
    print("No filename given. Using default.")
    filename="beta=1.0e+05-Am=1-Rm=inf.dat"


x=np.arange(0.3,10,0.02)
y=np.arange(-8.0,8.0,0.02)


# this function interpolates the spherical self-similar field stored
# in (ssCoords,ssFld), at the (r,theta) coordinates, using the self-similar exponent
# zeta
def mapSS(ssFld,ssCoords,theta,r,zeta):
    rf=r.flatten()
    thetaF=theta.flatten()
    shape=theta.shape
    f=interp1d(ssCoords,ssFld,bounds_error=False)
    mapFld=rf**zeta*f(thetaF)
    return(mapFld.reshape(shape))
    

# read the self-similar datafile  
def read_profile(filename):
    print("opening %s"%filename)
    #Open the file
    raw=np.loadtxt(filename,skiprows=7)
    prof={}
    prof['theta']=raw[:,0]
    prof['rho']=raw[:,1]
    prof['prs']=raw[:,2]
    prof['vx1']=raw[:,3]
    prof['vx2']=raw[:,4]
    prof['vx3']=raw[:,5]
    prof['bx1']=raw[:,6]
    prof['bx2']=raw[:,7]
    prof['bx3']=raw[:,8]
    prof['Am']=raw[:,9]
    prof['Rm']=raw[:,10]
    
    return prof
    
    
# this function maps the self-similar fields contained in prof
# at cylindrical coordinates (R2d,Z2d)

def make_2dfield(R2d,Z2d,prof):
    data={}
    #cread self-similar variable
    theta2d=np.arctan2(R2d,Z2d)
    r2d=np.sqrt(R2d**2+Z2d**2)
    data['rho']=mapSS(prof['rho'],prof['theta'],theta2d,r2d,-1.5)
    data['prs']=mapSS(prof['prs'],prof['theta'],theta2d,r2d,-2.5)
    data['vx1']=mapSS(prof['vx1'],prof['theta'],theta2d,r2d,-0.5)
    data['vx2']=mapSS(prof['vx2'],prof['theta'],theta2d,r2d,-0.5)
    data['vx3']=mapSS(prof['vx3'],prof['theta'],theta2d,r2d,-0.5)
    
    data['Bx1']=mapSS(prof['bx1'],prof['theta'],theta2d,r2d,-5.0/4.0)
    data['Bx2']=mapSS(prof['bx2'],prof['theta'],theta2d,r2d,-5.0/4.0)
    data['Bx3']=mapSS(prof['bx3'],prof['theta'],theta2d,r2d,-5.0/4.0)
    data['Am']=mapSS(prof['Am'],prof['theta'],theta2d,r2d,0)
    data['Rm']=mapSS(prof['Rm'],prof['theta'],theta2d,r2d,0)
    
    data['BR']=data['Bx1']*np.sin(theta2d)+data['Bx2']*np.cos(theta2d)
    data['BZ']=data['Bx1']*np.cos(theta2d)-data['Bx2']*np.sin(theta2d)
    
    data['vR']=data['vx1']*np.sin(theta2d)+data['vx2']*np.cos(theta2d)
    data['vZ']=data['vx1']*np.cos(theta2d)-data['vx2']*np.sin(theta2d)
    return data
    

#read data
prof=read_profile(filename)

# define the grid
[R2d,Z2d]=np.meshgrid(x,y,indexing='ij')

#create 2d self-similar fields
data=make_2dfield(R2d,Z2d,prof)

#########################################################
# have a look at mean field lines and stream lines
#########################################################

# Alfven speed
va=np.sqrt(data['Bx1']**2+data['Bx2']**2)/np.sqrt(data['rho'])
#poloidal velocity magnitude
vp=np.sqrt(data['vx1']**2+data['vx2']**2)
#cound speed
cs=np.sqrt(data['prs']/data['rho'])

# Mach Number
M=vp/cs

# Alfvenic Mach Number
Ma=vp/va

# Plasma beta
betap=2*data['prs']/(data['Bx1']**2+data['Bx2']**2)


V=1.5
plt.figure(figsize=(10,12))
plt.contourf(x,y,np.log10(M.T),64,cmap='RdBu_r',vmin=-V,vmax=V)
plt.colorbar()
plt.streamplot(x,y,data['vR'].T,data['vZ'].T,color='k',density=3)
plt.xlabel('R')
plt.ylabel('Z')
plt.title('V (color in Mach)')
plt.axis([x[0], x[-1],y[0],y[-1]])


plt.figure(figsize=(10,12))
plt.contourf(x,y,np.log10(data['rho']).T,64,cmap='gnuplot')
plt.colorbar()
plt.streamplot(x,y,data['BR'].T,data['BZ'].T,color='w',density=2)
plt.xlabel('R')
plt.ylabel('Z')
plt.title(r'B (color in $\log(\rho)$)')
plt.axis([x[0], x[-1],y[0],y[-1]])

plt.show()
