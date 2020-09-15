#!/bin/bash

#SBATCH --account=GT5DSTC  # Account number

#SBATCH -J try_dask        # job name
#SBATCH -N 11              # Number of nodes
#SBATCH -n 11              # The number of tasks (jobs)
#SBATCH -c 10              # logical cores per task
                           # (1 node: 80 logical, 40 physical)
#SBATCH --time 00:10:00    # hh|mm|ss
#SBATCH --mem 60GB         # Memory
#SBATCH -p S-M             # Job class
#SBATCH -o 0_launcher.out
#SBATCH -e 0_launcher.err

# Usage
# sbatch try_dask.cmd

# Number of nodes (cannot define before SBATCH commands)
NODES=11
echo $NODES

# Clean worker folder
WORKDIR="worker"
echo rm -r ./$WORKDIR*
rm -r ./$WORKDIR*
echo mkdir -p ./$WORKDIR
mkdir -p ./$WORKDIR

# Select scheduler
SCHEDULER=$(srun hostname | head -1)
echo $SCHEDULER

# Start scheduler
SCHEDFILE="cluster.json"
echo srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &
srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &

# Wait until scheduler is ready
sleep 20

# Start worker
WORKERS=$((NODES - 1))
echo srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory $WORKDIR
srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory $WORKDIR

echo HEUREKA

# If cluster is ready, you can use Client(scheduler_file='$SCHEDFILE')
# - In Jupyter Notebook on login node
# - In Python from login node
# - Or directly here:
# /home/dheim/miniconda3/bin/python try_dask.py
