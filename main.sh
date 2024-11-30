#!/bin/bash

CURRENT_DIR=$(dirname "$0")

echo "01 Medical institutions CSV file to GeoJSON file"
TIMER_START_01=$(date +%s)
{
  ${CURRENT_DIR}/.venv/bin/python 01_medical-institutions-csv2geojson.py
} || {
  echo "Error Found! Exiting.."
  exit 1
}
TIMER_END_01=$(date +%s)
echo "Elapsed Time: $(($TIMER_END_01-$TIMER_START_01)) seconds"

echo "02 Insert GeoJSON data to DB"
TIMER_START_02=$(date +%s)
{
    bash ${CURRENT_DIR}/02_insert-geojson-data-to-db.sh
} || {
  echo "Error Found! Exiting.."
  exit 1
}
TIMER_END_02=$(date +%s)
echo "Elapsed Time: $(($TIMER_END_02-$TIMER_START_02)) seconds"