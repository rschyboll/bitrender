#!/bin/bash
version=$1

function downloadLibraries {
    svn checkout "https://svn.blender.org/svnroot/bf-blender/tags/blender-$version-release/lib/linux_centos7_x86_64/"
}
cd "./downloads"

if [ -d "./lib" ]
then
    rm -rf "./lib"
fi
mkdir lib
cd "./lib"
downloadLibraries