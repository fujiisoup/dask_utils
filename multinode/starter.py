from dask.distributed import Client
import subprocess
import os
import time
import multinode.sbatch as sbatch
import multinode.scluster as scluster


def _get_paths():
    pid = os.getpid()
    job_path = "multinode-{}".format(pid)
    if not os.path.exists(job_path):
        os.makedirs(job_path)
    worker_path = os.path.join(job_path, "worker")
    if not os.path.exists(worker_path):
        os.makedirs(worker_path)
    return job_path, worker_path


def run_script(account_name, job_name, n_workers,
               n_cores, run_time, mem, job_class):
    out_path, worker_path = _get_paths()
    cluster_file = os.path.join(out_path, "cluster.json")
    # Create script
    s = sbatch.get_sbatch(account_name, job_name, n_workers,
                          n_cores, run_time, mem, job_class,
                          out_path)
    s += scluster.get_scluster(n_workers, worker_path,
                               cluster_file)
    # Write script
    starter_script = '{}/starter-script.cmd'.format(out_path)
    with open(starter_script, 'w') as file:
        file.write(s)
    # Start script
    subprocess.Popen(['sbatch', starter_script],
                     stdout=subprocess.PIPE, universal_newlines=True)
    return cluster_file


def start_client(cluster_file, n_workers):
    cluster = Client(scheduler_file=cluster_file)
    cluster.wait_for_workers(n_workers)


def get_dash_addr(cluster):
    scheduler_info = cluster.scheduler_info()
    dash_addr = scheduler_info['address']
    dash_addr = dash_addr.split(':')
    dash_addr = dash_addr[1][2:] + ":" + \
        str(scheduler_info['services']['dashboard'])
    return dash_addr


def start_cluster(account_name, job_name, n_workers,
                  n_cores, run_time, mem, job_class):

    cluster_file = run_script(account_name, job_name, n_workers,
                              n_cores, run_time, mem, job_class)
    cluster = start_client(cluster_file, n_workers)
    dash_addr = get_dash_addr(cluster)

    return cluster, dash_addr
