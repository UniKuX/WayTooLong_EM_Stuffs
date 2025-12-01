# Relion v5 for GPU with Intel CPUs

## Create a sandbox using relion5_gpu_intel_base.def:

```text
sudo singularity build relion5_gpu_intel_base.sif relion5_gpu_intel_base.def
sudo singularity build --sandbox gpu_base/ relion5_gpu_intel_base.sif
```

## Use a writable shell:

N.B. If --no-home does not work, add the ctffind tar.gz to the /root dir on the build machine

```text
sudo singularity shell --no-home --writable gpu_base/
```

## Complete the steps in the shell:

```text
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
apt update
apt install intel-mkl
echo $MKLROOT
export CPATH="/usr/include/mkl/fftw:/usr/include/mkl"
export MKLROOT=/usr/include/mkl
export PATH="/opt/miniconda-latest/bin:$PATH"
conda_installer="/tmp/miniconda.sh"
curl -fsSL -o "$conda_installer" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash "$conda_installer" -b -p /opt/miniconda-latest
rm -f "$conda_installer"
conda update -yq -nbase conda
conda config --system --prepend channels conda-forge
conda config --set channel_priority strict
conda config --system --set auto_update_conda false
conda config --system --set show_channel_urls true
conda init bash
source /root/.bashrc
conda deactivate
conda create -n relion-test -y
sync && conda clean --all --yes && sync
rm -rf ~/.cache/pip/*
rm -rf ctffind-4.1.14
tar -xzf ctffind-4.1.14.tar.gz
mkdir /root/ctffind-4.1.14/build
cd /root/ctffind-4.1.14/build
/root/ctffind-4.1.14/configure
make
make install
cd /opt
git clone https://github.com/3dem/relion.git
cd relion
git checkout ver5.0
echo $MKLROOT
echo $CPATH
conda env create -f /opt/relion/environment.yml
mkdir /opt/torch
cd /opt/relion/build
mkdir /opt/Movies
mkdir /users
useradd --no-user-group --create-home --shell /bin/bash nonroot
cmake -DMKLFFT=ON -DTORCH_HOME_PATH=/opt/torch -DCUDA=ON -DCUDA_ARCH=80 -DFETCH_WEIGHTS=OFF -DCMAKE_INSTALL_PREFIX=/usr/local/ /opt/relion/
make
make install
relion
```

## Build a sif from the sandbox:

```text
sudo singularity build relion5_gpu_intel.sif gpu_base/
```

## Example incantation to run on CREATE HPC

Bind descriptions:
Weights have previously been downloaded to /datasets/relion5/torch/
Relion .sh submission scripts are in /scratch/prj/atherton_group_processing/relion_script
Wrapper for sbatch mapped to /usr/bin/sbatch to allow Relion running in Singularity container to submit jobs called from submission scripts
Make the data for processing available to the container

```text
singularity shell --nv \
  --bind /datasets/relion5/torch:/opt/torch \
  --bind /scratch/prj/atherton_group_processing/relion_script \
  --bind /scratch/prj/atherton_group_processing/relion_script/sbatch_gpu:/usr/bin/sbatch \
  --bind /scratch/prj/atherton_group_processing/Tom_Foran/Data/kif1A-KBP_single_complex \
  /software/containers/singularity/relion/relion5_gpu_intel.sif
```
