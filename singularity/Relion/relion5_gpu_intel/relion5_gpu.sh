#!/bin/bash
#SBATCH --output=XXXoutfileXXX
#SBATCH --error=XXXerrfileXXX
#SBATCH --ntasks=XXXmpinodesXXX
#SBATCH --nodes=1
#SBATCH --gres gpu:1
#SBATCH -p XXXqueueXXX
#SBATCH --chdir=CREATE_PWD
#SBATCH --constraint=XXXextra1XXX

#module load openmpi
mpiexec XXXcommandXXX
