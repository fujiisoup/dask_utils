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

    # Popen does not wait, but how do I know WHEN all nodes are there and then workers connected?
    # e.g. check_call does wait, but when command ends: all resouces canceled
    subprocess.Popen(['sbatch', 'multinode/try_dask_{}.cmd'.format(pid)],
                     stdout=subprocess.PIPE, universal_newlines=True)

    client = Client(scheduler_file='cluster.json')
    client.wait_for_workers(nodes-2)
    time.sleep(5)

    return client


# Interactive multiprocess
#
# thread = multiprocessing.Process(target=start_cluster)
# thread.start()
# time.sleep(10)
# thread.terminate()

# subprocess.check_output()
#
# res = check_output('salloc -J try_dask  -N 1 -n 1 -c 10 --account=GT5DSTC --time 00:10:00 --qos interactive;' +
#                     'srun dask-scheduler --interface ipogif0 --scheduler-file cluster.json',
#                     stderr=STDOUT, shell=True)
# print(res)

# Popen
#
# proc = subprocess.Popen('salloc -J try_dask  -N 1 -n 1 -c 10 --account=GT5DSTC --time 00:10:00 --qos interactive')
# proc.communicate()
# proc.wait()
