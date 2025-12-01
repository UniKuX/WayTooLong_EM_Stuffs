# Using Relion container on CREATE

Once the final sif container is built it will need to be transferred to create.

There is a directory for Relion containers in `/software/containers/singularity/`

mv the built container into the dir and at least chgrp to er_hpc_admins.

Suggested permissions are 0775.

## previous comm to users

```text
To use the singularity container for Relion v5, at the moment it is very geared for a specific group and I will look at how we can make it more generic although they have been instrumental in testing and developing the scripts.

# Starting with a standard ssh config for CREATE HPC as recommended in our documentation
# (https://docs.er.kcl.ac.uk/CREATE/access/#using-an-ssh-config-file-mac-os-and-linux),
# ~/.ssh/config with the additional entry added for direct access to a node once allocated (using srun or salloc - srun is covered here)
Host create
    Hostname hpc.create.kcl.ac.uk
    User <k-number>
    PubkeyAuthentication yes
    IdentityFile <path-to-ssh-key>

# Additional .ssh/config entry for direct access to nodes  
Host erc-hpc-comp*
      User <k-number>
      ProxyJump create

# on HPC (comp198 was showing an error so had to exclude it)
srun -p interruptible_gpu --gres=gpu:1 --pty /bin/bash -l

# on local computer command line connect direct to the allocated node
ssh -X erc-hpc-comp<allocated_node_num>

# on erc-hpc-comp<allocated_node_num>
# will only need to do this once
mkdir -p /scratch/users/${USER}/singularity/cache

# could add this to .bashrc although I prefer not to make too many changes to my .bashrc so use it each time
export SINGULARITY_CACHEDIR=/scratch/users/${USER}/singularity/cache

# making sure there is enough space in a SINGULARITY_TMPDIR (can be deleted after the work is finished and is not always needed)
export SINGULARITY_TMPDIR=/scratch/users/${USER}/singularity/tmp
mkdir -p $SINGULARITY_TMPDIR

# change into a suitable project dir
cd /path/to/relion5/project/dir

# use the container
singularity shell --nv \
  --bind /datasets/relion5/torch:/opt/torch \
  --bind /scratch/prj/atherton_group_processing/relion_script \
  --bind /scratch/prj/atherton_group_processing/relion_script/sbatch_gpu:/usr/bin/sbatch \
  --bind /scratch/prj/atherton_group_processing/Tom_Foran/Data/kif1A-KBP_single_complex \
  /software/containers/singularity/relion/relion5_gpu_intel.sif

Descriptions of the binds:
Weights have previously been downloaded to /datasets/relion5/torch/ to reduce the size of the container
Relion .sh submission scripts are in /scratch/prj/atherton_group_processing/relion_script
Wrapper for sbatch mapped to /usr/bin/sbatch to allow Relion running in Singularity container to submit jobs called from submission scripts
Make the data for processing available to the container

A bug has been reported when trying to use the Napari viewer:
An untested workaround is to run the following command in the Singularity shell:
export QT_QPA_PLATFORM=offscreen
```
