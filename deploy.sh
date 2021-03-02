#!/bin/sh

#build react
cd purpl3_rms
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
cp ../deployment/wsgi.py Purpl3_Giraffe_RMS
cp ../deployment/Purpl3_RMS.ini Purpl3_Giraffe_RMS
cp -r ../purpl3_rms/build/* Purpl3_Giraffe_RMS/web
cp -r ../res  Purpl3_Giraffe_RMS/res

#startup in virutal enviorment 
source Purpl3_Giraffe_RMS/bin/activate

#insall deps
pip install wheel
pip install uwsgi flask

#port it will be running on
sudo ufw allow 5000

