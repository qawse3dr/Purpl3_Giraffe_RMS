#!/bin/bash
#AUTHOR: PURPL3_RMS INC
if [ ! -d ~/.ssh ]
then
  mkdir ~/.ssh
fi

echo $sshkey >> ~/.ssh/authorized_keys
