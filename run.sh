#!/bin/sh
#shouldnt be used as it will make both applications
cd purpl3_rms
npm run-sript start &
cd ..

python Purpl3_RMS.py &