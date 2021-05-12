#!/bin/bash

# deploy

cd ~/attollo
source attolloenv/bin/activate
cd Attollo
git stash
git pull git@github.com:parkersell/Attollo.git
cd attollo
pip install -r requirements.txt | grep -v 'already satisfied'
systemctl restart gunicorn
