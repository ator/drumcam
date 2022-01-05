#!/bin/bash
./startcam.sh 1 /dev/video2
./startcam.sh 2 /dev/video4
./startcam.sh 3 /dev/video6
./startcam.sh 4 /dev/video8
read -p "Press any key to stop..."
killall ffmpeg
