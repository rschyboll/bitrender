#!/bin/bash
function downloadBlender {
    git clone https://git.blender.org/blender.git
}

function updateSubmodules {
    git submodule update --init --recursive
    git submodule foreach git checkout master
    git submodule foreach git pull --rebase origin master
}

function updateRepository {
    git pull --rebase
    git pull --rebase origin master
    git submodule foreach git pull --rebase origin master   
}

function makeUpdate {
    make update
}


if [ -d "./downloads" ] 
then
    cd "./downloads"
    if [ ! -d "./blender" ]
    then
        downloadBlender
        cd "./blender"
        updateSubmodules
        
    else 
        cd "./blender"
        updateRepository
    fi
    makeUpdate
else
    mkdir "./downloads"
    cd "./downloads"
    downloadBlender
    cd "./blender"
    updateSubmodules
    makeUpdate
fi
