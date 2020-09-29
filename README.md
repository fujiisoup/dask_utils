# multinode package

This package allows to allocate a Dask scheduler and its workers at once.
In this way
- The scheduler lives as long as the workers
- All Dask HW is allocated in one sbatch request

## TODOs
- [x] Return actual dashboard-address or write to file
- [x] Test dashboard
- [x] Create setup.py
- [x] Test install with pip -e and import in file outside of this repo
- [ ] Make documentation
  - Docstrings
  - Example usage
  - Output file descritp
- [ ] Beautify code
- [ ] Add more info to command line output
- [ ] Add tests
