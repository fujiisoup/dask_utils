from multinode import starter
from dask.distributed import Client
import time

# TODO: Keisuke-Whishlist
# - Write template script and sbatch it (instad of modifying template)
# - Add dashboard-address wish as argument
# - Return actual dashboard-address or write to file
# - Add get_client() arguments: cluster specific infos (e.g. nb of nodes)
# - scheduler_file_name
# - ((((Make class: Member variables: srun parameters (e.g. project name))?))
# - Make documentation
# - Make multiple clusters runnable


scheduler_file_name = starter.start_cluster(nodes=5)

client = Client(scheduler_file=scheduler_file_name)
client.wait_for_workers(3)
time.sleep(5)

print(client)
print("hi")
