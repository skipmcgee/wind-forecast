#!/bin/bash
# this is a cron job to automate getting sensor 
# and forecast data in to your database
# recommended to run hourly
# arg: first and only arg is the address to the web app
# like format test.org:3000/ 
defaultaddress="127.0.0.1:3000"
scriptargs="$@"
sensorlist=( 1 2 )
modellist=( 1 2 )

mycurl="$(which curl)"
echo "Starting add_data_cron with args: ${scriptargs}"
if [ "${scriptargs[@]}" > 0 ]; 
then
    echo "** add_data_cron using custom location ${scriptargs[0]}"
    for key in "${!sensorlist[@]}"
        do
        for key in "${!modellist[@]}"
            do
            echo "** adding Sensor: ${sensorlist[$key]}, Model: ${modellist[$key]}"
            curl -s -o /dev/null -w "%{http_code}\n" -k -X POST "http://${scriptargs[0]}/add/forecast/${sensorlist[$key]}/${modellist[$key]}"
            curl -s -o /dev/null -w "%{http_code}\n" -k -X POST "http://${scriptargs[0]}/add/reading/${sensorlist[$key]}"
            done
        done
else
    echo "** add_data_cron using standard location $defaultaddress"
    for key in "${!sensorlist[@]}"
        do
        for key in "${!modellist[@]}"
            do
            echo "** adding Sensor: ${sensorlist[$key]}, Model: ${modellist[$key]}"
            curl -s -o /dev/null -w "%{http_code}\n" -k -X POST "http://$defaultaddress/add/forecast/${sensorlist[$key]}/${modellist[$key]}"
            curl -s -o /dev/null -w "%{http_code}\n" -k -X POST "http://$defaultaddress/add/reading/${sensorlist[$key]}"
            done
        done
fi

echo "Ending add_data_cron" 
