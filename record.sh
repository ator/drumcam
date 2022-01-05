#!/bin/bash
date=`date +%Y%m%d-%H%M`
outdir=takes/$date
outfile=$outdir/cam$1.avi
logfile=$outdir/cam$1.log
framerate=60
#framerate=30
#framerate=15
size=1920x1080
#size=1280x720
#size=640x360
#size=320x180
mkdir -p $outdir
echo "ffmpeg -hide_banner -loglevel warning -f v4l2 -r $framerate -s $size -input_format mjpeg -i /dev/video$1 -r 60 -vcodec copy -y $outfile &" > $logfile
ffmpeg -hide_banner -loglevel warning -f v4l2 -r $framerate -s $size -input_format mjpeg -i /dev/video$1 -r 60 -vcodec copy -y $outfile >> $logfile 2>&1 &
