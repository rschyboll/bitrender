#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
cd ..


if [[ -f "./downloads/build_linux_bpy/bin/bpy.so" ]]
then
    sitePackages=$1
    if [[ -d $sitePackages ]]
    then
        cd "./downloads"
        if [[ -d "./build_linux_bpy" ]]
        then
            cd "./build_linux_bpy"
            #echo /home/hoodrobinrs/Dokumenty/Rendering_Server/venv/lib/python3.7/site-packages
            cmake ../blender \
                    -DCMAKE_INSTALL_PREFIX=$sitePackages \
                    -DWITH_INSTALL_PORTABLE=ON 
            make install
        else
            echo "Build bpy first"
        fi
    else
        echo "Directory does not exist"
    fi
else
    echo "Build bpy first, then install to venv"
fi