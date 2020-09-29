from dask_ml.decomposition import PCA
import dask.array as da
from multinode import starter
import time

# Example allocation of Dask client
cluster, dash_addr = starter.start_cluster(
    account_name="GT5DSTC",
    job_name="multinode",
    n_workers=10,
    n_cores=10,
    run_time="00:10:00",
    mem="60GB",
    job_class="S-M")
print("Cluster info: {}".format(cluster))
print("- Dashboard address: {}".format(dash_addr))

# Example rund: PCA with 240 GB
# - On login node: 57 s
# - On cluster: 25 s
print("Start example")
x = da.random.random((100000, 300000), chunks=(10000, 10000))
print("- {} GB".format(x.nbytes/1e9))
pca = PCA(n_components=2)
start = time.time()
pca.fit(x)
end = time.time()
print("- Vars: {}".format(pca.explained_variance_ratio_))
print("- Time: {} s".format(end-start))
