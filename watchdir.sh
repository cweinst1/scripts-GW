#! /usr/bin/env bash
########################################################################
##  Usage:
##  watchdir.sh <directory path>
##
##  File ID:      watchdir.sh
##
##  Description:  This script checks every 60 minutes for new files in 
##                the specified directory
##
##  Inputs:       Path to directory to watch
##
##  Outputs:      Outputs new files to stdout
##                Updates FILELIST and NEWLIST with new list of files
##
########################################################################
##
##                        Modification Log
##
##  Author              Version     Date           Comments
##  Colin Weinstein     1.0         02/18/2022     Initial version
##
########################################################################

FILELIST=$HOME/develop/data/filelist
NEWLIST=$HOME/develop/data/filelist2
#MONITOR_DIR=/export/customer/dstn/prod/data/claims/input/$1
MONITOR_DIR=$HOME/develop/log/$1

[[ -f ${FILELIST} ]] || ls -m ${MONITOR_DIR} | sed "s/, /~/g" | tr '~' '\n' | sed "s/,//g" > ${FILELIST}
[[ -f ${NEWLIST} ]]  || ls -m ${MONITOR_DIR} | sed "s/, /~/g" | tr '~' '\n' | sed "s/,//g" > ${NEWLIST}

while : ; do
  ls -m ${MONITOR_DIR} | sed "s/, /~/g" | tr '~' '\n' | sed "s/,//g" > ${NEWLIST}
  # Check for new files
  diff <(cat ${FILELIST}) <(cat $NEWLIST) 1>/dev/null || \
    { echo "Alert: ${MONITOR_DIR} changed" 
      # Output new files
      comm -3 ${FILELIST} ${NEWLIST}
      # Overwrite old file list with the new one.
      cat ${NEWLIST} > ${FILELIST}
    }
  # Waits 60 minutes before next check
  echo "Waiting for changes."
  sleep $(expr 60 \* 60)
done

