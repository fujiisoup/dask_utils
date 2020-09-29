# multinode package

This package allows to allocate a scheduler and all workers of a Dask client at once.
In this way
- The scheduler lives as long as the workers
- The Dask client is allocated earlier in clusters where large jobs are preferrec (compared to single node allocations)

## TODOs
- [x] Return actual dashboard-address or write to file
- [x] Test dashboard
- [ ] Create Setup.py
- [ ] Test install with pip -e and import in file outside of this repo
- [ ] Make documentation
  - Docstrings
  - Example usage
  - Output file descritp
- [ ] Beautify code
- [ ] Add more info to command line output
