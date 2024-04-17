#!/bin/bash

# install deps
sudo apt update -y
sudo apt install -y wget git python3 python3-venv libgl1 libglib2.0-0 ffmpeg nano nginx google-perftools python3-pip yt-dlp yasm nasm libx265-dev libnuma-dev libvpx-dev libfdk-aac-dev libmp3lame-dev libopus-dev build-essential libx264-dev nodejs npm speedtest-cli

# install deoldify
git clone https://github.com/mayeaux/colorize
cd colorize
pip install -r requirements.txt
cd models
wget https://data.deepai.org/deoldify/ColorizeVideo_gen.pth

cd ~
# install ffmpeg from source
wget https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
./configure --prefix=/usr/local --enable-gpl --enable-libx264 --enable-shared
make
sudo make install

echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/ffmpeg/libavdevice:/usr/local/lib' >> ~/.bashrc
echo 'export NUMEXPR_MAX_THREADS=$(nproc)' >> ~/.bashrc
source ~/.bashrc
npm install -g http-server

cd ~/colorize
mkdir -p video/source
cd video/source
