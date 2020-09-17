
def get_scluster(nodes, worker_path, cluster_file):
    return """
# Select scheduler name
SCHEDULER=$(srun hostname | head -1)

# Start scheduler
srun -N 1 -n 1 --nodelist=$SCHEDULER \
    dask-scheduler --interface ipogif0 --scheduler-file {} &

# Wait until scheduler is ready
sleep 20

# Start workers
srun -N {} -n {} --exclude=$SCHEDULER \
    dask-worker --scheduler-file {} --local-directory {}

""".format(cluster_file, (nodes-1), (nodes-1), cluster_file, worker_path)
