# multinode package

This package allows to allocate a scheduler and all workers of a Dask client at once.
In this way
- The scheduler lives as long as the workers
- The Dask client is allocated earlier in clusters where large jobs are preferrec (compared to single node allocations)

## TODOs
- [x] Test dashboard
- [ ] Add dashboard-address wish as argument
- [ ] Return actual dashboard-address or write to file
- [ ] Beautify code
- [ ] Make documentation
  - Docstrings
  - Example usage
- [ ] Create Setup.py
- [ ] Test install with pip -e and import in file outside of this repo
