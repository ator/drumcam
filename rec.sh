#!/bin/bash
./record.sh 2
./record.sh 4
./record.sh 6
./record.sh 8
read -p "Press any key to stop..."
killall ffmpeg
