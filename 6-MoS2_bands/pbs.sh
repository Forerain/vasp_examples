#!/bin/sh -f

#PBS -N example6
#PBS -l nodes=1:ppn=4
#PBS -q ib
#PBS -e error

nprocs=`wc -l < $PBS_NODEFILE`
cd $PBS_O_WORKDIR

/opt/intel/impi/4.1.0.024/intel64/bin/mpirun -genv I_MPI_DEVICE rdma -np $nprocs /opt/bin/vasp.5.2.12 > stdout
