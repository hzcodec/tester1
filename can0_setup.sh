BITRATE=$1

ip link set up can0 type can bitrate $BITRATE restart-ms 100
