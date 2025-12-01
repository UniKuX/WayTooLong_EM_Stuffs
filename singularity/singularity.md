# Singularity containers on CREATE HPC

Singularity Image Files (.sif) are found in the path `/software/containers/singularity/`

The current provided .sifs are for:

- Ansys (fluent): may need to be guarded by access group (er_grp_ansys_fluent) as NMES purchased the license
- epap
- NeoDisc: guarded by access group (er_grp_neodisc) as requires licensing
- Relion
- RStudio
- TensorFlow

Singularity is useful for strict reproducability and making applications with GUIs available.

## Building a .sif

A [gitlab repo](https://gitlab.er.kcl.ac.uk/ops/singularity_defs) is available with definitions used so far in (some are yet to be added).
Instructions and resources (or links to them) should be stored with the definitions to allow anyone to be able to build and run the containers on the HPC.
They may also be useful as references for when building containers for different applications.

To build a .sif it is recommended to create an instance in OpenStack.

Building can require quite considerable resources in terms of storage as well as CPU and RAM.

One approach is to have the base server (e.g. 8cpu16ram) with singularity installed and then add volumes as required for each application (that can then be recycled).

## Create a basic Singularity environment

```text
sudo apt update && sudo apt upgrade -y
sudo reboot
sudo apt-get install -y autoconf automake build-essential cryptsetup fuse fuse2fs git libfuse-dev libglib2.0-dev libseccomp-dev libtool pkg-config runc squashfs-tools squashfs-tools-ng uidmap wget zlib1g-dev
wget https://go.dev/dl/go1.22.3.linux-amd64.tar.gz
sudo tar -C /usr/local -xzvf go1.22.3.linux-amd64.tar.gz
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
export VERSION=4.1.3
wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-ce-${VERSION}.tar.gz
tar -xzf singularity-ce-${VERSION}.tar.gz
cd singularity-ce-${VERSION}
./mconfig
make -C ./builddir
sudo make -C ./builddir install
```

### Adding a volume

Create a volume in OpenStack and attach it to the instance

On the instance:

```text
# check existing mounts
mount
# list block devices available
sudo lsblk
# for ease of copying and pasting
export THIS_APP=NeoDisc
# create a directory for the mount
sudo mkdir -p /singularity/${THIS_APP}
# create a file system on the attached device
sudo mkfs -t ext4 /dev/vdb
# mount the new file system at the created path
sudo mount /dev/vdb /singularity/${THIS_APP}
# persist the mount by adding to fstab
sudo sed -i "$ a /dev/vdb /singularity/${THIS_APP} ext4 defaults,noatime 0 0" /etc/fstab
# check it was added as expected
cat /etc/fstab
# make the directory world accessible
sudo chmod 0777 /singularity/${THIS_APP}
```

## Making .sif available on HPC

```text
# Create a directory for the application
mkdir /software/containers/singularity/neodisc
# mv the sif to the directory
# can directly rsync from local machine
# permissions will need to be set
# for world readable
chmod -R 0775 /software/containers/singularity/neodisc
# to restrict to a group
chgrp -R er_grp_neodisc /software/containers/singularity/neodisc
chmod -R 0750 /software/containers/singularity/neodisc
```
