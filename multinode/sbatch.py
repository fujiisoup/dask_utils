
def get_sbatch(nodes, job_path):
    return """#!/bin/bash

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

""".format(nodes, nodes, job_path, job_path)
