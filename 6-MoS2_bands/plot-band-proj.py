#!/usr/bin/env python
from datetime import datetime

import numpy as np
import matplotlib as mpl
mpl.use("PDF")
import pylab as pl

def main():
    title='MoS$_2$-1ML (VASP-PAW-PBE.Mo_pv)'
    xlabel=['$\mathrm{\Gamma}$','$\mathrm{K}$','$\mathrm{M}$','$\mathrm{\Gamma}$']
    xlabelpos=[1, 21, 31, 48]
    ylimit=[-6.5,5.5]
    yminor=4 
    [nkpt,nband,nion,kpt,ev,proj]=read_procar()
    efermi = get_efermi()
    [econ,eval]=find_edges(ev,efermi+1)
    eshift=eval

    fig=pl.gcf()
    fig.set_size_inches(5,6)
    fig.subplots_adjust(bottom=0.05,left=0.12, top=0.94, right=0.96)
    fig.set_dpi(300)
    fig.suptitle(title,fontsize=13)
    ax = pl.gca()
    mpl.rcParams['font.sans-serif']='Arial' #'Helvetica'
    pl.ylabel('Energy (eV)',fontsize=12)
    pl.xticks(xlabelpos,xlabel,size=12)
    pl.yticks(size=10)
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(yminor))
    pl.autoscale(enable=True,axis='y')
    pl.tick_params(axis='y',which='major',direction='out',length=3, width=0.8,left='on',right='off',pad=5)
    pl.tick_params(axis='y',which='minor',direction='out',length=2, width=0.5,left='on',right='off')
    pl.tick_params(axis='x',which='both',top='off',bottom='off')
    for xline in xlabelpos:
        pl.axvline(x=xline,color='k',linewidth=0.6)
    x=np.arange(ev.shape[1])+1
    for i in range(ev.shape[0]):
        pl.plot(x,ev[i,:]-eshift,'k-')

    plot_projection(proj,ev,[1],[5,6,7,8,9],eshift,'b')
    plot_projection(proj,ev,[2,3],[2,3,4],eshift,'r')
    pl.scatter(-99,-99,marker='o',c='b',alpha=0.5,label='Mo d')
    pl.scatter(-99,-99,marker='o',c='r',alpha=0.5,label='S p')

    pl.xlim(x.min(),x.max())
    pl.ylim(ylimit)
    pl.axhline(y=eval-eshift,color='g',linestyle='--')
    pl.axhline(y=econ-eshift,color='g',linestyle='--')
    mpl.rcParams['pdf.fonttype']=42
    pl.legend(loc=1,prop={'size':8})
    pl.savefig('band_proj.pdf')
    
def get_efermi(filename='OUTCAR'):
    for l in open(filename,'r'):
        if l.find('E-fermi')!=-1:
            efermi=float(l.split()[2])
    return efermi

def search_bands(ev):
    band_top=[]
    band_bottom=[ev[1,:].min()]
    for i in range(ev.shape[0]-1):
        d=ev[i+1,:]-ev[i,:]
        if d.min()>0.01:
            band_top.append(ev[i,:].max())
            band_bottom.append(ev[i+1,:].min()) 
    band_top.append(ev[ev.shape[0]-1,:].max())
    return [band_top,band_bottom]

def find_edges(s,ef):
    eup = s.max()
    elow= s.min()
    for i in range(s.shape[0]):
        for j in range(s.shape[1]):
            diff=s[i,j]-ef
            if (diff>0) and (diff<eup-ef):
                eup=s[i,j]
            if (diff<0) and (diff>elow-ef):
                elow=s[i,j]
    return [eup,elow]

def read_procar(fname="PROCAR"):
    """Read a VASP PROCAR file"""
    f = open(fname)
    f.readline()
    line=f.readline().split()
    nkpt=int(line[3])
    nband=int(line[7])
    nion=int(line[11])
    kpt=np.zeros([nkpt,3])
    ev=np.zeros([nband,nkpt])
    proj=np.zeros([nband,nkpt,nion+1,10])
    f.readline()
    for ik in range(nkpt):
        line=f.readline().split()
        kpt[ik,:]=np.array([float(x) for x in line[3:6]])
        f.readline()
        for ib in range(nband):
            line=f.readline().split()
            ev[ib,ik]=float(line[4])
            f.readline()
            f.readline()
            for ia in range(nion+1):
                line=f.readline().split()
                proj[ib,ik,ia,:]=np.array([float(x) for x in line[1:]])
            f.readline() 
        f.readline()
    return [nkpt,nband,nion,kpt,ev,proj]

def plot_projection(proj,ev,latom,lorb,eshift,color,threshold=0.2,scale=100):
    nband=ev.shape[0]
    nkpt =ev.shape[1] 
    for ib in range(nband):
        for ik in range(nkpt):
            sum_proj=0.0
            for ia in latom:
                for io in lorb:
                    sum_proj+=proj[ib,ik,ia-1,io-1]
                if sum_proj>=threshold:
                    pl.scatter(ik+1,ev[ib,ik]-eshift,s=sum_proj**2*scale,marker='o',c=color,alpha=.5,edgecolor=color,lw=0.1)

main()
