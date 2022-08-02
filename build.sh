#! /usr/local/bin/bash

# get current directory
currentDir=`pwd`

declare -a jobsToAdd

jobsToAdd+=("0 0 * * * python3 $currentDir/fetch_runner.py")
jobsToAdd+=("0 0 * * * python3 $currentDir/daily_email_runner.py")
jobsToAdd+=("0 0 * * 0 python3 $currentDir/weekly_email_runner.py")

# install all dependencies
pip3 install -r requirements.txt

# setup automations
(crontab -l 2> /dev/null; printf "%s\n" "${jobsToAdd[@]}") | sort -u | crontab

echo "All good!"
