#!/bin/sh -f

#PBS -N example2
#PBS -l nodes=1:ppn=4
#PBS -q ib
#PBS -e error

nprocs=`wc -l < $PBS_NODEFILE`
cd $PBS_O_WORKDIR

rm -f SUMMARY
for a in 3.56 3.58 3.60 3.62 3.64 3.66 3.68 3.70 3.72 
   do 
      echo "a = $a"   
      mkdir $a
      cp INCAR $a
      cp KPOINTS $a
      cp POTCAR $a
      sed s/LATTICE/$a/ POSCAR.0 > $a/POSCAR
      cd $a
      /opt/intel/impi/4.1.0.024/intel64/bin/mpirun -genv I_MPI_DEVICE rdma   -np $nprocs  /opt/bin/vasp.5.2.12 > stdout
      E=`tail -1 OSZICAR | awk '{print $5}'`
      cd ..
      echo $a   $E >>SUMMARY
   done

vasp/5.4.1/intel-mpi-5.0.2.044_intel-compiler-2015.1.133