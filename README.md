# Multinode package

This package allows to allocate a Dask scheduler and its workers at once.
In this way
- The scheduler lives as long as the workers
- All Dask HW is allocated in one sbatch request


## Setup
- Clone: ```git clone https://github.com/fujiisoup/dask_utils.git```
- Enter folder: ```cd dask_utils```
- Install ```pip install -e .```

## Usage

### Example
```python
from multinode import starter

client, dash_addr = starter.start_cluster(
    account_name="GT5DSTC",
    job_name="multinode",
    n_workers=10,
    n_cores=10,
    run_time="00:10:00",
    mem="60GB",
    job_class="S-M")

# Use Dask: E.g. dask_ml.decomposition.PCA.fit()
```

### Arguments
- **n_workers**: Number of Dask workers
- **n_cores**: Number of cores for each worker
- **run_time**: Format: "HH:MM:SS"
- **mem**: Format: "xxGB"

### Returns
- **client**: dask.distributed.Client
- **dash_addr**: Dasboard address, e.g. ```"10.128.2.48:8787"```

### Output files
In each run, a folder ```./multinode-<ID>/``` is created. It contains the files
- **starter-script.cmd**: SBATCH script used by multinode
- **launcher.out**: Scheduler stdout
- **launcher.err**: Scheduler stderr
- **cluster.json**: Dask cluster config file

and the folder
- **worker/**: One folder for each worker containing its stderr

## TODOs
- [x] Return dashboard-address
- [x] Check if dashboard-address works
- [x] Create setup.py
- [x] Test install with pip -e and import in file outside of this repo
- [x] Make documentation
  - Write example usage
  - Add output file description
- [ ] Beautify code
  - Add Docstrings
- [ ] Add more info to command line output
- [ ] Add tests
- [ ] Use job ID instead of PID
- [ ] Add function stop_cluster()
- [ ] Add timeout to waiting for cluster to be initialized
