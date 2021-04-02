#!/bin/bash

#build react
cd purpl3_rms
npm install
npm run-script build
cd ..

#clean deploy folder
rm -rf deploy

#make deployment
mkdir deploy
cd deploy

#create vm
python -m venv Purpl3_Giraffe_RMS

#create file structure
mkdir -p Purpl3_Giraffe_RMS/web

#cp files to deployment
cp -r ../libpurpl3 Purpl3_Giraffe_RMS
cp ../Purpl3_RMS.py Purpl3_Giraffe_RMS
cp ../Purpl3_CMD.py Purpl3_Giraffe_RMS
cp ../config.yaml Purpl3_Giraffe_RMS
cp ../deployment/wsgi.py Purpl3_Giraffe_RMS
cp ../deployment/Purpl3_RMS.ini Purpl3_Giraffe_RMS
cp ../purpl3_rms.db Purpl3_Giraffe_RMS
cp -r ../deployment Purpl3_Giraffe_RMS
cp -r ../purpl3_rms/build/* Purpl3_Giraffe_RMS/web
cp -r ../res  Purpl3_Giraffe_RMS/res
cp -r ../data Purpl3_Giraffe_RMS

#startup in virutal enviorment 
source Purpl3_Giraffe_RMS/bin/activate

#insall deps
pip install wheel
pip install uwsgi flask pyyaml paramiko

#port it will be running on
sudo ufw allow 5000

