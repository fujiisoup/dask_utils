from dask_ml.decomposition import PCA
import dask.array as da
from multinode import starter
import time

# Example: PCA with 240 GB
# - On login node: 57 s
# - On cluster: 25 s

cluster = starter.start_cluster(
    account_name="GT5DSTC",
    job_name="multinode",
    n_workers=10,
    n_cores=10,
    run_time="00:10:00",
    mem="60GB",
    job_class="S-M")
print(cluster)

print("start example")
x = da.random.random((100000, 300000), chunks=(10000, 10000))
print(x.nbytes/1e9)
pca = PCA(n_components=2)
start = time.time()
pca.fit(x)
end = time.time()
print(pca.explained_variance_ratio_)
print(str(end-start) + " seconds")
