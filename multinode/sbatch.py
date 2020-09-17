

def get_sbatch(account_name, job_name, n_workers,
               n_cores, run_time, mem, job_class, job_path):
    n_nodes = n_workers+1
    return """#!/bin/bash

#SBATCH --account={}  # Account name
#SBATCH -J {}         # Job name
#SBATCH -N {}         # Number of nodes
#SBATCH -n {}         # The number of tasks (jobs)
#SBATCH -c {}         # Logical cores per task
#SBATCH --time {}     # hh|mm|ss
#SBATCH --mem {}      # Memory
#SBATCH -p {}         # Job class
#SBATCH -o {}/launcher.out
#SBATCH -e {}/launcher.err

""".format(account_name, job_name, n_nodes,
           n_nodes, n_cores, run_time, mem, job_class,
           job_path, job_path)
