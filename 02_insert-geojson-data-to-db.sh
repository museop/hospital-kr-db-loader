#!/bin/bash


echo "Insert DB data"

ogr2ogr -f "PostgreSQL" PG:"host=localhost user=myuser dbname=mydb password=mypassword" kr_medical_institutions.geojson -nln medical_institutions -append

echo "Inserted sussefully"
