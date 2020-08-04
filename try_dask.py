import time
import xarray as xr
import humanize

from dask_ml.decomposition import PCA
from dask.distributed import Client

with open('hello.txt', 'w') as the_file:
    the_file.write("hello")

print("Init cluster")
client = Client(scheduler_file='cluster.json')

print("Load data")
base_folder_path = ("/project/GYROPT/yasahi/MachineLearning/" +
                    "f5D_analysis/DJ_FD_ITGTEM_2MW_NU1/f5D_sp1/")
print("- base_folder_path: {}".format(base_folder_path))
nfiles = 10
print("- nfiles: {}".format(nfiles))
files = []
for n in range(nfiles):
    # Avoid using the very first data
    files.append(base_folder_path + "f5D_sp1_t{}.nc".format(1040 + n*2))

data_org = xr.open_mfdataset(files, concat_dim='time', combine='nested')
print("- Sizes: {}".format(data_org.sizes))

data_org2 = xr.open_mfdataset(files,
                              chunks={'wg': 2},
                              compat='no_conflicts', concat_dim='time',
                              combine='nested', parallel=True)

print(data_org2['f5D'].data)
print("- Datasize: {}".format(humanize.naturalsize(
    data_org2['f5D'].data.nbytes)))
print("- Chunksize: {}".format(humanize.naturalsize(
    data_org2['f5D'].data.nbytes / data_org2['f5D'].data.npartitions)))
print("- Sizes: {}".format(data_org2.sizes))

print("Stack data")
data_org2 = data_org2.stack(sample=['time', 'phig', 'rg', 'thetag'])
data_org2 = data_org2.stack(feature=['vparg', 'wg'])
print(data_org2['f5D'].data)

print("Do PCA")
pca = PCA(n_components=64)
start = time.time()
pca.fit(data_org2['f5D'].data)
print(pca.explained_variance_)
end = time.time()
print('- It took {} s'.format(end - start))

# construct xarray object
result = xr.Dataset({'mean': ('feature', pca.mean_),
                     'basis': (('latent', 'feature'), pca.components_)},
                    coords={'feature': data_org2['feature'],
                            'sample': data_org2['sample']},
                    attrs={'file_start': files[0],
                           'file_stop': files[-1]})
result = result.unstack().to_netcdf(
    '/project/GYROPT/dheim/pca_result-files_1040-2-features_vparg_phig_time.nc')
end = time.time()
print('- It took {} s'.format(end - start))
