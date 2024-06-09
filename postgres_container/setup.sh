#!/usr/bin/bash

PG_DATA_DIR_NAME="pg_temp_data"
PG_DATA_FULLPATH="/tmp/${PG_DATA_DIR_NAME}"

if [[ (-f /bin/mkdir || -f /usr/bin/mkdir) && -d /tmp ]];
then
  echo "Creating ${PG_DATA_DIR_NAME} directory under /tmp";
  mkdir -p ${PG_DATA_FULLPATH}

  chmod -R 777 ${PG_DATA_FULLPATH}
  if [[ -d ${PG_DATA_FULLPATH} ]];
  then
    echo "Setup done - ${PG_DATA_DIR_NAME} created."
    exit 0
  fi
else
  echo "Could not create ${PG_DATA_DIR_NAME} directory under /tmp - exiting."
  exit 1
fi