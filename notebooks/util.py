import numpy as np

# Import dask
import dask

# Use dask jobqueue
from dask_jobqueue import PBSCluster

def get_pbscluster(nthreads):
    
    cluster = PBSCluster(
        cores=1, # The number of cores you want
        memory='10GB', # Amount of memory
        processes=1, # How many processes
        queue='casper', # The type of queue to utilize (/glade/u/apps/dav/opt/usr/bin/execcasper)
        local_directory='$TMPDIR', # Use your local directory
        resource_spec='select=1:ncpus=1:mem=10GB', # Specify resources
        project='CESM0002', # Input your project ID here
        walltime='04:00:00', # Amount of wall time
        interface='ib0', # Interface to use
    )
    # Scale up
    cluster.scale(nthreads)
    
    dask.config.set({'distributed.dashboard.link':'https://jupyterhub.hpc.ucar.edu/stable/user/{USER}/proxy/{port}/status'})

    return cluster

# a function to return the global mean of a dataset
# variables weighted by cos(latitude)
#
def global_mean(ds):
    lat = ds['lat']
    weight = np.cos(np.deg2rad(lat))
    weight /= weight.mean()
    other_dims = set(ds.dims) - {'year'}
    
    return (ds * weight).mean(other_dims)

