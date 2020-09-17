
def get_scluster(nodes, worker_path, cluster_file):
    return """
# Select scheduler
SCHEDULER=$(srun hostname | head -1)
echo $SCHEDULER

# Start scheduler
SCHEDFILE="{}"
echo srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &
srun -N 1 -n 1 --nodelist=$SCHEDULER dask-scheduler --interface ipogif0 --scheduler-file $SCHEDFILE &

# Wait until scheduler is ready
sleep 20

# Start worker
WORKERS=$(({} - 1))
echo srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory {}
srun -N $WORKERS -n $WORKERS --exclude=$SCHEDULER dask-worker --scheduler-file $SCHEDFILE --local-directory {}

""".format(cluster_file, nodes, worker_path, worker_path)
