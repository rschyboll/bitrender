#!/bin/bash
task=$1

case $task in

  BPY)
    cp ./.vscode/bpy_tasks.json ./.vscode/tasks.json
    ;;

  CLIENT)
    cp ./.vscode/client_tasks.json ./.vscode/tasks.json
    ;;

  SERVER)
    cp ./.vscode/server_tasks.json ./.vscode/tasks.json
    ;;

esac