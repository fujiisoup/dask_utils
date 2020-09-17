from dask_ml.decomposition import PCA
import dask.array as da
from multinode import starter
import time

# TODO: Keisuke-Whishlist
# - Write template script and sbatch it (instad of modifying template)
# - Add dashboard-address wish as argument
# - Return actual dashboard-address or write to file
# - Add get_client() arguments: cluster specific infos (e.g. nb of nodes)
# - scheduler_file_name
# - Make documentation, example in readme.md
# - Make multiple clusters runnable (prefix: python pid (todo: slurm pid))
# - Create python package (Setup.py, install with pip -e
# - Test import in file outside of this repo


client = starter.start_cluster(nodes=10)
print(client)

# Example: PCA with 240 GB
# - On login node: 57 s
# - On cluster, 10 nodes, each 10 C and 60GB: 25 s
print("start example")
x = da.random.random((100000, 300000), chunks=(10000, 10000))
print(x.nbytes/1e9)
pca = PCA(n_components=2)
start = time.time()
pca.fit(x)
end = time.time()
print(pca.explained_variance_ratio_)
print(str(end-start) + " seconds")
