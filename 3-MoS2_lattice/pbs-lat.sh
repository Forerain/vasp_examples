#!/bin/sh -f

#PBS -N example3
#PBS -l nodes=1:ppn=4
#PBS -q ib
#PBS -e error

nprocs=`wc -l < $PBS_NODEFILE`
cd $PBS_O_WORKDIR

rm -f SUMMARY
for a in 3.15 3.16 3.17 3.18 3.19 3.20 3.21 3.22 3.23  
   do 
      echo "a = $a"   
      mkdir $a
      cp INCAR $a
      cp KPOINTS $a
      cp POTCAR $a
      sed 2s/.*/$a/ POSCAR.0 > $a/POSCAR
      cd $a
      /opt/intel/impi/4.1.0.024/intel64/bin/mpirun -genv I_MPI_DEVICE rdma   -np $nprocs  /opt/bin/vasp.5.2.12 > stdout
      E=`tail -1 OSZICAR | awk '{print $5}'`
      cd ..
      echo $a   $E >>SUMMARY
   done
