#!/usr/bin/env python
import numpy as np
from sys import argv,exit    # argv=argument variable参数变量
import os.path

def main():
    if len(argv) == 1:
        dir = '.'
    elif len(argv) == 2:
        dir = argv[1]
    else:
        print "Usage: glocpotc [path]"
        exit(0)
    fn_locpot = dir + '/LOCPOT'
    if os.path.isfile(fn_locpot):
        lattice_constant,a,elements,numofatoms,atom_pos,locpot = read_locpot(fn_locpot)
        potz = np.empty([locpot.shape[2]+1])
        for z in range(locpot.shape[2]):
            potz[z] = locpot[:,:,z].sum()/locpot.shape[0]/locpot.shape[1]
            sz = np.linalg.norm(a[2])*lattice_constant
        potz[locpot.shape[2]] = potz[0]
        dpotz = np.empty([locpot.shape[2]])
        for z in range(locpot.shape[2]):
            dpotz[z] = (potz[z+1]-potz[z-1])/2
            print '{0:5d} {1:8.4f} {2:12.6f} {3:12.6f}'.format(z,float(z)/locpot.shape[2],potz[z],dpotz[z])
	print 'Max:{0:12.6f}'.format(potz.max())
#        plot_locpot_z(lattice_constant,a,elements,numofatoms,atom_pos,locpot)

    else:
        print 'File {} does not exist!'.format(fn_locpot)
    
def read_locpot(filename='LOCPOT'):
    """Read LOCPOT
    """
    f = open(filename)
    
    # read title
    title = f.readline()

    # read lattice constant
    lattice_constant = float(f.readline().split()[0])

    # read the lattice vectors
    a = np.empty([3,3])
    for ii in range(3):
        s = f.readline().split()
        a[ii] = float(s[0]), float(s[1]), float(s[2])
    
    # read atom types
    elements = f.readline().split()

    # Check whether we have a VASP 4.x or 5.x format file. If the
    # format is 5.x, use the fifth line to provide information about
    # the atomic symbols.
    vasp5 = False
    try:
        int(elements[0])
        print filename,' is not in VASP 5.x format!'
        return
    except ValueError:
        vasp5 = True

    # read number of atoms
    numofatoms = f.readline().split()
    for i, num in enumerate(numofatoms):
        numofatoms[i] = int(num)
    tot_atoms = sum(numofatoms)

    f.readline()
        
    # read atom coordinates
    atom_pos = np.empty([tot_atoms, 3])
    for atom in xrange(tot_atoms):
        ac = f.readline().split()
        atom_pos[atom] = float(ac[0]), float(ac[1]), float(ac[2])

    # read local potential
    f.readline()
    ngr = f.readline().split()
    locpot = np.empty([int(ngr[0]), int(ngr[1]), int(ngr[2])])
    for zz in range(locpot.shape[2]):
        for yy in range(locpot.shape[1]):
            locpot[:, yy, zz] = np.fromfile(f, count = locpot.shape[0], sep=' ')
    f.close()
    return lattice_constant,a,elements,numofatoms,atom_pos,locpot
    
def plot_locpot_z(lattice_constant,a,elements,numofatoms,atom_pos,locpot):
    import matplotlib as mpl
    mpl.use("PDF")
    import pylab as pl
    potz = np.empty([locpot.shape[2]])
    for z in range(locpot.shape[2]):
        potz[z] = locpot[:,:,z].sum()/locpot.shape[0]/locpot.shape[1]
#        print '{0:4d} {1:12.6f}'.format(z,potz[z])
    sz = np.linalg.norm(a[2])*lattice_constant
#    print potz.max()
    
    # Plot Setting 
    pl.title('LOCPOT',size=12)
    pl.xlabel('Z',size=10)
    pl.ylabel('Local potential (eV)',size=10)
    xminor = 4
    yminor = 4

    fig=pl.gcf()
    fig.set_size_inches(5,3)
    fig.subplots_adjust(bottom=0.14,left=0.12, top=0.88, right=0.95)
    fig.set_dpi(300)
    mpl.rcParams['font.sans-serif']='Arial'
    ax = pl.gca()
    ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(xminor))
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(yminor))
    pl.xticks(size=8)
    pl.yticks(size=8)
    pl.tick_params(axis='x',which='major',direction='in',length=3, width=1,top='on',bottom='on',pad=6)
    pl.tick_params(axis='y',which='major',direction='in',length=3, width=1,left='on',right='on',pad=6)
    pl.autoscale(enable=True,axis='x')
    pl.autoscale(enable=True,axis='y')

    # Plot
    z = np.arange(potz.shape[0])/float(potz.shape[0])
    pl.plot(z,potz,'-',label='locpot_z')
#    pl.legend(loc=1,prop={'size':8})
    pl.savefig('locpot_z.pdf')
    
    return
    
main()
