# Relion Singularity build notes

## Relion5_cpu_amd

Version has been built as a container and runs with no known issues

## Relion5_gpu_amd

Version has been built as a container although not used as all the nodes requested with GPUs have intel CPUs

## Relion5_gpu_intel

More details and an additional README in the dir

TODO: Reported bug (add xcb packages in relion5_gpu_intel_base.def)

```text
There is an error when relion v5 operating in tomography version tries to use the Napari viewer. Something to do with python, any ideas (see below)?

---------------------------------- PYTHON ERROR ---------------------------------
   Has RELION been provided a Python interpreter with the correct environment?
   The interpreter can be passed to RELION either during Cmake configuration by
     using the Cmake flag -DPYTHON_EXE_PATH=<path/to/python/interpreter>.
---------------------------------------------------------------------------------

  Using python executable: /opt/miniconda-latest/envs/relion-5.0/bin/python

WARNING: Could not load the Qt platform plugin "xcb" in "" even though it was found.
WARNING: This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

/usr/local/bin/relion_python_tomo_exclude_tilt_images: line 30: 3147088 Aborted                 (core dumped) "$python_executable" -c "from tomography_python_programs.exclude_tilt_images import cli; exit(cli())" "$@"
```
