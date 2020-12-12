#!/bin/bash

function downloadBlender {
    echo "Downloading blender source"
    git clone https://git.blender.org/blender.git
    cd "./blender"
    git submodule update --init --recursive
    git submodule foreach git checkout master
    git submodule foreach git pull --rebase origin master
    cd ..
}

function downloadLibraries {
    echo "Downloading blender libraries"
    mkdir "./lib"
    cd "./lib"
    svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64
    cd ..
}

function getBlenderVersion {
    if [[ ! $(git ls-remote --tags https://git.blender.org/blender.git -l "$version") ]]; then
        echo "Wrong blender version."
        exit
    fi
}

function checkoutToVersion {
    cd "./downloads/blender"
    git config pull.rebase true
    git config advice.detachedHead false
    git pull --rebase
    git submodule foreach git pull --rebase origin master
    git checkout "tags/$version"
    git submodule update --recursive
    cd ..
    cd ..
}

function pullUpdates {
    cd "./downloads/blender"
    git fetch
    cd ..
    cd ..
}

function update {
    cd "./downloads/blender"
    make update
    cd ..
    cd ..
}

function build {
    cd "./downloads/blender"
    make bpy
    cd ..
    cd ..
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
version=$1
cd ..

getBlenderVersion

if [ -d "./downloads" ] 
then
    cd "./downloads"
    if [ ! -d "./blender" ]
    then
        downloadBlender
    fi
    if [ ! -d "./linux_centos7_x86_64" ]
    then
        downloadLibraries
    fi
else
    mkdir "./downloads"
    cd "./downloads"
    downloadBlender
    downloadLibraries
fi
cd ..

pullUpdates
checkoutToVersion

update
build
