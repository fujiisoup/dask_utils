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


scheduler_file_name = starter.start_cluster(nodes=10)

client = Client(scheduler_file=scheduler_file_name)
client.wait_for_workers(8)
time.sleep(5)

print(client)
print("hi")

# Example: PCA with 240 GB
# - On login node: 57 s
# - On cluster, 10 nodes, each 10 C and 60GB: 25 s

import numpy as np
import dask.array as da
from dask_ml.decomposition import PCA
x = da.random.random((100000, 300000), chunks=(10000, 10000))
print(x.nbytes/1e9)
pca = PCA(n_components=2)
start = time.time()
pca.fit(x)
end = time.time()
print(pca.explained_variance_ratio_)
print(str(end-start) + " seconds")
