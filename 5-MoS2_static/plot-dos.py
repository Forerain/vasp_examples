#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use("PDF")
import pylab as pl

def main():
    title='MoS$_2$-1ML (VASP-PAW-PBE.Mo_pv)'
    xlimit=[-7,6]
    ylimit=[0,8]                
    xminor=5 
    yminor=2 

    [natoms,nedos,efermi,tdos,pdos]= read_doscar('DOSCAR') 
    pl.plot(tdos[:,0]-efermi,tdos[:,1],'b-')
    
    pl.axvline(x=0.0,color='g',linewidth=0.6)
    fig=pl.gcf()
    fig.suptitle(title,fontsize=11)
    fig.set_size_inches(5,3)
    fig.subplots_adjust(bottom=0.14,left=0.11, top=0.91, right=0.97)
    fig.set_dpi(300)
    ax = pl.gca()
    ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(xminor))
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(yminor))
    mpl.rcParams['font.sans-serif']='Arial' #'Helvetica'
    pl.xlabel('Energy (eV)',fontsize=11)
    pl.ylabel('DOS',fontsize=11)
    pl.xticks(size=10)
    pl.yticks(size=10)
    pl.xlim(xlimit)
    pl.ylim(ylimit)
    pl.tick_params(axis='x',which='major',direction='in',length=3, width=0.8,top='on',bottom='on',pad=5)
    pl.tick_params(axis='x',which='minor',direction='in',length=2, width=0.5,top='on',bottom='on',pad=5)
    pl.tick_params(axis='y',which='major',direction='in',length=2, width=0.8,left='on',right='off',pad=5)
    pl.tick_params(axis='y',which='minor',direction='in',length=1, width=0.5,left='on',right='off',pad=5)

#    pl.savefig('tdos.pdf')


def read_doscar(fname="DOSCAR"):
    """Read a VASP DOSCAR file"""
    f = open(fname,'r')
    natom = int(f.readline().split()[0])
    [f.readline() for nn in range(4)]  # Skip next 4 lines.
    # total and total integrated DOS
    line_6=f.readline().split()
    ndos = int(line_6[2])
    efermi = float(line_6[3])
    tmp = []
    for nd in xrange(ndos):
        tmp.append(np.array([float(x) for x in f.readline().split()]))
    tdos = np.array(tmp)
    line=f.readline()
    dos = []
    if line:
        for i in range(natom):
            tmp = []
            for j in range(ndos):
                tmp.append([float(x) for x in f.readline().split()])
            f.readline()
            dos.append(tmp)
    pdos = np.array(dos)
    print pdos.shape
    f.close()
    return [natom,ndos,efermi,tdos,pdos]    
main()

