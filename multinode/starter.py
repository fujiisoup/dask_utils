from dask.distributed import Client
import subprocess
import time
import os
import multinode.sbatch as sbatch


def start_cluster(nodes: int):
    pid = os.getpid()
    s = sbatch.get_sbatch(nodes)
    with open('multinode/try_dask_{}.cmd'.format(pid), 'w') as file:
        file.write(s)

    # Popen does not wait for process end
    subprocess.Popen(['sbatch', 'multinode/try_dask_{}.cmd'.format(pid)],
                     stdout=subprocess.PIPE, universal_newlines=True)

    client = Client(scheduler_file='cluster.json')
    client.wait_for_workers(nodes-2)
    time.sleep(5)

    return client
