

def get_sbatch(nodes, job_path, worker_path, cluster_file):
    s = """#!/bin/bash

#SBATCH --account=GT5DSTC  # Account number

#SBATCH -J try_dask        # job name
#SBATCH -N {}              # Number of nodes
#SBATCH -n {}              # The number of tasks (jobs)
#SBATCH -c 10              # logical cores per task
                           # (1 node: 80 logical, 40 physical)
#SBATCH --time 00:10:00    # hh|mm|ss
#SBATCH --mem 60GB         # Memory
#SBATCH -p S-M             # Job class
#SBATCH -o {}/launcher.out
#SBATCH -e {}/launcher.err

# Number of nodes (cannot define before SBATCH commands)
NODES={}
echo $NODES

# Select scheduler
SCHEDULER=$(srun hostname | head -1)
echo $SCHEDULER

# Start scheduler
SCHEDFILE="{}"
echo srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &
srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &

# Wait until scheduler is ready
sleep 20

# Start worker
WORKERS=$((NODES - 1))
echo srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory {}
srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory {}

""".format(nodes, nodes, job_path, job_path, nodes, cluster_file, worker_path, worker_path)
    return s
