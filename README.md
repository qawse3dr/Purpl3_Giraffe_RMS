# Purpl3_Giraffe_RMS

by: James, Larry, Soory, DAniela, Rachel, Julian

This is our 3750 project

## Deps
python3 and flask needed to run

```
python3
venv #might already be installed

```
### Install flask using pip
python -m pip install flask

## Running
backend will run on port http://localhost:8080
frontend will run on port http://localhost:3000
note when using the app connect to http://localhost:3000 backend will be passed by proxy for connection

``` 
#backend
cd backend
python Purple3_RMS.py
cd ..

#frontend
cd purpl3_rms
npm run-script start
```
## deployment only use for production for development use proxy
#creates a deploy folder containing all the files needed for deployment
./deploy.sh

#copy conf files remember to change paths to your setup
copy systemd service to /etc/systemd/system/rms.service
copy rms_nginx.conf to /etc/nginx/enabled-sites

#start services
sudo systemctl reload-daemon 
sudo systemctl reload nginx
sudo systemctl start nginx
sudo systemctl start rms

#connect to website on 
http://rms.localhost
