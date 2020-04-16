#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use("PDF")
import pylab as pl
import os

def main():
    pl.title('MoS$_2$-1ML (VASP-PAW-PBE.Mo_pv)',fontsize=12)
    xlabel=['$\mathrm{\Gamma}$','$\mathrm{K}$','$\mathrm{M}$','$\mathrm{\Gamma}$']
    xlabelpos=[1,21,31,48]
    ef = get_efermi()
    ylimit=[-7,6]
    yminor=4 

    fig=pl.gcf()
    fig.set_size_inches(5,6)
    fig.subplots_adjust(bottom=0.05,left=0.12, top=0.95, right=0.96)
    fig.set_dpi(300)
    ax = pl.gca()
    mpl.rcParams['font.sans-serif']='Arial' #'Helvetica'
    pl.ylabel('Energy (eV)',fontsize=10)
    pl.xticks(xlabelpos,xlabel,size=10)
    pl.yticks(size=9)
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(yminor))
    pl.autoscale(enable=True,axis='y')
    pl.tick_params(axis='y',which='major',direction='out',length=4, width=1,left='on',right='off',pad=5)
    pl.tick_params(axis='y',which='minor',direction='out',length=3, width=0.5,left='on',right='off')
    pl.tick_params(axis='x',which='both',top='off',bottom='off')
    for xline in xlabelpos:
        pl.axvline(x=xline,color='k',linewidth=0.6)
    ev=read_eigenvalues_vasp()
    x=ev[0,:]
    econ,eval=find_edges(ev,ef)
    print 'E_fermi: {0}   Band edges: {1} {2}'.format(ef,econ,eval)
    for i in range(ev.shape[0]-1):
        pl.plot(x,ev[i+1,:]-eval,'k-')
    pl.xlim(x.min(),x.max())
    pl.ylim(ylimit)
    pl.axhline(y=econ-eval,color='g',linestyle='--')
    pl.axhline(y=0.0,color='g',linestyle='--')
    mpl.rcParams['pdf.fonttype']=42
    pl.savefig('band.pdf')

def get_efermi():
    """Method that reads Fermi energy from OUTCAR file"""
    E_f=None
    f_outcar='OUTCAR'
    if os.path.exists(f_outcar):
        for line in open(f_outcar, 'r'):
            if line.find('E-fermi') > -1:
                E_f=float(line.split()[2])
    else:
        print 'OUTCAR does not exist!'
    return E_f

def find_edges(s,ef):
    eup = s.max()
    elow= s.min()
    for i in range(1,s.shape[0]):
        for j in range(s.shape[1]):
            diff=s[i,j]-ef
            if (diff>0) and (diff<eup-ef):
                eup=s[i,j]
            if (diff<0) and (diff>elow-ef):
                elow=s[i,j]
    return [eup,elow]

    
def read_eigenvalues_elk(filename='BAND.OUT'):
    nband=0
    nkpt=0
    colx=np.array([])
    coly=np.array([])
    for line in open(filename, 'r'):
        fields = line.strip().split()
        if len(fields)==0:
            nband=nband+1
        else:
            coly=np.append(coly,float(fields[1]))
            if nband==0:
                colx=np.append(colx,float(fields[0]))
    coly=coly.reshape(nband,-1)
    return np.vstack((colx,coly))

def read_eigenvalues_vasp(filename='EIGENVAL'):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    nspin=int(lines[0].split()[3])
    nkpt=int(lines[5].split()[1])
    nband=int(lines[5].split()[2])
    klist= np.arange(nkpt)+1.
    eigs = []
    for i in range(nkpt):
        for j in range(nband):
            for s in range(nspin):
                eigs.append(float(lines[8+i*(nband+2)+j].split()[s+1]))
    ev=np.array(eigs).reshape(nkpt,-1).transpose()
    return np.vstack((klist,ev))

def read_eigenvalues_qe(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    nkpt=int(lines[0].split()[4])
    nband=int(lines[0].split()[2].rstrip(','))
    klist= np.arange(nkpt)+1.
    eigs = []
    for s in lines[1:]:
        if s.strip()!='':
            eigs.extend(map(float,s.split()))
    ev=np.array(eigs).astype(np.float)
    for i in range(nkpt):
        k=np.arange(3)+i*nband
        ev=np.delete(ev,k)
    ev=ev.reshape(nkpt,-1).transpose()
    return np.vstack((klist,ev))

main()
