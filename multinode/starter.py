from dask.distributed import Client
import subprocess
import time
import os
import multinode.sbatch as sbatch
import multinode.scluster as scluster


def start_cluster(nodes: int):
    pid = os.getpid()

    job_path = "multinode-{}".format(pid)
    if not os.path.exists(job_path):
        os.makedirs(job_path)
    worker_path = os.path.join(job_path, "worker")
    if not os.path.exists(worker_path):
        os.makedirs(worker_path)

    cluster_file = os.path.join(job_path, "cluster.json")

    s = sbatch.get_sbatch(nodes, job_path)
    s += scluster.get_scluster(nodes, worker_path, cluster_file)

    starter_script = '{}/starter-script-{}.cmd'.format(job_path, pid)
    with open(starter_script, 'w') as file:
        file.write(s)

    # Popen does not wait for process end
    subprocess.Popen(['sbatch', starter_script],
                     stdout=subprocess.PIPE, universal_newlines=True)

    client = Client(scheduler_file=cluster_file)
    client.wait_for_workers(nodes-2)
    time.sleep(5)

    return client
