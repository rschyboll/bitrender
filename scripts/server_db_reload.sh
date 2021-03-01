#!/bin/bash
source ../../venv/bin/activate

pgmodeler-cli -if server_model.dbm -ed -dd --conn-alias local-db

cd ..
cd ./backend
cd ./src
cd ./models
