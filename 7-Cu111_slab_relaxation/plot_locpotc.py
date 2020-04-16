#!/usr/bin/env python
# Last modified on Jul.19,2014
import numpy as np
import os

def main():
    # Get E_fermi
    if os.path.exists('OUTCAR'):
        ef = get_efermi()
    else:
        print 'OUTCAR does not exist!'
        exit(0)
    print 'Ef:',ef

    # Get c axis
    if os.path.exists('CONTCAR'):
        sc = get_axis_c()
    else:
        print 'CONTCAR does not exist!'
        exit(0)
    print 'sc:',sc
    
    # Read locpotc.dat
    if os.path.exists('locpotc.dat'):
        lpc = read_locpotc('locpotc.dat')
    else:
        print 'locpotc.dat does not exist!'
        exit(0)
    plot_locpotc(lpc,ef,sc)
    
def read_locpotc(filename='locpotc.dat'):
    lpc = []
    for line in open(filename, 'r'):
        if len(line.split()) == 4:
            lpc.append(np.array([float(x) for x in line.split()]))
    return np.array(lpc)
    
def plot_locpotc(lpc,ef,sc):
    import matplotlib as mpl
    mpl.use("PDF")
    import pylab as pl
    
    # Plot Setting 
#    pl.title('LOCPOT',size=12)
    pl.xlabel('c axis ($\mathrm{\AA}$)',size=12)
    pl.ylabel('Local potential (eV)',size=12)
    xminor = 5
    yminor = 5

    fig=pl.gcf()
    fig.set_size_inches(6,4)
    fig.subplots_adjust(bottom=0.13,left=0.10, top=0.96, right=0.97)
    fig.set_dpi(300)
    mpl.rcParams['font.sans-serif']='Arial'
    ax = pl.gca()
    ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(xminor))
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(yminor))
    pl.xticks(size=10)
    pl.yticks(size=10)
    pl.tick_params(axis='x',which='major',direction='in',length=3, width=1,top='on',bottom='on',pad=6)
    pl.tick_params(axis='y',which='major',direction='in',length=3, width=1,left='on',right='on',pad=6)
    ax.margins(0.1)
    pl.autoscale(enable=True,axis='x')
    pl.autoscale(enable=True,axis='y')
    pl.xlim([0,sc])
    
    # Plot
    pl.plot(lpc[:,1]*sc,lpc[:,2]-ef,'-',label='locpot_c')
    pl.axhline(y=0.0,color='g',linestyle='--')
#    pl.legend(loc=1,prop={'size':8})
    pl.savefig('locpotc.pdf')
    
    return

def get_efermi():
    E_f = None
    f_outcar = 'OUTCAR'
    for line in open(f_outcar, 'r'):
        if line.find('E-fermi') > -1:
            E_f = float(line.split()[2])
    return E_f

def get_axis_c(filename='CONTCAR'):
    f = open(filename)
    title = f.readline()
    lattice_constant = float(f.readline().split()[0])
    a = np.empty([3,3])
    for ii in range(3):
        s = f.readline().split()
        a[ii] = float(s[0]), float(s[1]), float(s[2])
    sc = np.linalg.norm(a[2]) * lattice_constant
    f.close()
    return sc

main()