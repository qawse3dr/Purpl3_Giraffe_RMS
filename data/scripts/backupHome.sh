#!/bin/bash

#creates backupFolder if it doesnt exist
mkdir -p "/backups"

#Find valid folder name
folderNum=1
while [ -d "/backups/backup"$folderNum ]
do
  folderNum=$(($folderNum + 1))
done

#create backupFolder
backupFolderName="/backups/backup"$folderNum
mkdir $backupFolderName

echo $backupFolderName
#copies file
rsync -av --progress ~ $backupFolderName --exclude .cache