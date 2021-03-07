# Deployment configs

## Purpl3_RMS.ini
conf file for wsgi used for deploying backend

## rms_nginx.conf
conf file for nginx linking front and backend
NOTE: you must change values in here to point to your project directory

## rms.service
systemd service running wsgi application and creating a port
NOTE: you must change values in here to point to your project directory

## wsgi.py
wsgi wrapper for the application
