#!/usr/bin/env python
# Last modified on Jul.16,2014
import numpy as np
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
from sys import argv,exit        # this sentence is like to transfer a parameter, argv is a list of variables
import os

if (len(argv)==1):
    in_summary = 'SUMMARY'     # bring the first volumn of SUMMARY to in_summary
elif (len(argv)==2):
    in_summary = argv[1]
else:
    print 'Usage: plot-lattice.py [SUMMARY]'
    exit(0)

if os.path.exists(in_summary):    
    x0,y0 = np.loadtxt(in_summary,unpack=True)
else:
    print 'ERROR: File {} does not exist!'.format(in_summary)
    exit(0)

#in_fit = 'fit.dat'
#if os.path.exists(in_fit):    
#    xfit,yfit=np.loadtxt(in_fit,unpack=True)
#else:
#    print 'ERROR: File {} does not exist!'.format(in_fit)
#    exit(0)

# Plot Setting 
fig = plt.figure()
fig.set_size_inches(7,6)
axes = fig.add_axes([0.15, 0.12, 0.80, 0.80])
font = {'family' : 'sans-serif',
        'color'  : 'Black',
        'weight' : 'normal',
        'size'   : 14,
        }

plt.title('Cu fcc bulk (VASP-PAW-PBE)',fontdict=font)
axes.set_xlabel('Lattice constant ($\AA$)',fontdict=font,fontsize=14)
axes.set_ylabel('Total energy (eV)',fontdict=font,fontsize=14)

axes.minorticks_on()
axes.tick_params(axis='x',which='major',bottom='on',length=5,width=1,pad=8,labelsize=12)
axes.tick_params(axis='y',which='major',left='on',length=5,width=1,pad=10,labelsize=12)

axes.tick_params(axis='x',which='both',top='off')
axes.tick_params(axis='x',which='minor',bottom='on',length=3,width=0.5)
axes.tick_params(axis='y',which='minor',left='on',length=3,width=0.5)
axes.tick_params(axis='y',which='both',right='off')

axes.set_xmargin(0.02)
axes.set_ymargin(0.02)
axes.autoscale()

# Plot
#axes.plot(xfit,yfit,'r-')
axes.plot(x0,y0,'bo',markersize=10)

fig.savefig('lattice.pdf')

