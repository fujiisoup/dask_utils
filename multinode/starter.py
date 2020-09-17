from dask.distributed import Client
import subprocess
import time
import os


def start_cluster(nodes: int):
    # Read in the file
    with open('multinode/try_dask.cmd', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('-N 11', '-N '+str(nodes))
    filedata = filedata.replace('-n 11', '-n '+str(nodes))
    filedata = filedata.replace('NODES=11', 'NODES='+str(nodes))

    # Write the file out again
    pid = os.getpid()
    with open('multinode/try_dask_{}.cmd'.format(pid), 'w') as file:
        file.write(filedata)

    # Popen does not wait, but how do I know WHEN all nodes are there and then workers connected?
    # e.g. check_call does wait, but when command ends: all resouces canceled
    cmd = subprocess.Popen(['sbatch', 'multinode/try_dask_{}.cmd'.format(pid)],
                           stdout=subprocess.PIPE, universal_newlines=True)

    return 'cluster.json'


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
