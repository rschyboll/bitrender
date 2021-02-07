#!/bin/bash
source ../../venv/bin/activate

pgmodeler-cli -if server_model.dbm -ed -dd --conn-alias local-db
pgmodeler-cli -if server_model.dbm -ef -dd -of server_model.sql

schemas=("user" "worker" "task")

cd ..
cd ./backend
cd ./src
cd ./models

read -p "Do you want to reload SQLAlchemy models? [Y/N]: " Validate
echo $Validate
if [ "$Validate" == "Y" ]; then
    for i in ${!schemas[@]}; do
        sudo -E -u postgres sqlacodegen --nojoined postgresql:///rendering_server --schema ${schemas[$i]} > __${schemas[$i]}.py
    done
fi
