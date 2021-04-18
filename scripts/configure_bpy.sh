#!/bin/bash

optix_location=$1

cd ./downloads/blender/build_files/cmake/config

if [ ! -f "./bpy_module_original.cmake" ]
then
    cp "bpy_module.cmake" "bpy_module_original.cmake"
fi

cp "bpy_module_original.cmake" "bpy_module.cmake"

function addConfig() {
    name=$1
    value=$2
    echo >> "./bpy_module.cmake"
    echo "set($name    $value CACHE BOOL \"\" FORCE)" >> "./bpy_module.cmake"
}

function addConfigString() {
        name=$1
    value=$2
    echo >> "./bpy_module.cmake"
    echo "set($name    $value CACHE STRING \"\" FORCE)" >> "./bpy_module.cmake"
}

addConfig "WITH_MEM_JEMALLOC" "OFF"

addConfig "WITH_CYCLES_CUDA_BINARIES" "ON"

addConfigString "CYCLES_CUDA_BINARIES_ARCH" "sm_35;sm_37;sm_50;sm_52;sm_60;sm_61;sm_70;sm_75;compute_75"

addConfig "WITH_CYCLES_DEVICE_OPTIX" "ON"

addConfigString "OPTIX_ROOT_DIR" $optix_location

