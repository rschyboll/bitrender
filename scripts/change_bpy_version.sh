#!/bin/bash
version=$1

function checkoutBlender {
    git config advice.detachedHead false
    git checkout "tags/$version"
    git submodule update --recursive
}

cd "./downloads"
cd "./blender"

checkoutBlender
