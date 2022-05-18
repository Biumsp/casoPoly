#$ -S /bin/bash
#$ -l h_rt=168:00:00
#$ -q erc_shape.q
#$ -e job.err
#$ -o job.out
#$ -pe mpi_8 8
#$ -cwd

### INFO ###
# The script works as following:
# 1/ Set up the case folder whatever you want but not in the scratch
# 2/ Define the path of you scratch folder by setting the SCRATCH variable
# 3/ Submit the job, the calculations will be performed on the scratch
#    and the result will be copied back in the command folder
# 4/ Please clean your scratch folder once the calculations are finished


source /software/energia2/OpenFOAM/OpenFOAM-5.x/etc/bashrc
export LD_LIBRARY_PATH=/software/chimica2/libraries/boost/boost-1.69.0-gcc-4.8.5/lib/:$LD_LIBRARY_PATH

mpirun -np 8 catalyticReactingEulerFoamMOS_NEW -parallel 1>> log 2> err

#################### DO NOT MODIFY #####################################
rm core.*
#rsync -azr . $OF
####################################################################
