#!/bin/bash

download=true
upload=true

case "$1" in
        --download)
            download=true
            upload=false
            ;;
        --upload)
            download=false
            upload=true
            ;;
    esac

while true; do
    

    if [ "$download" = true ] && [ "$upload" = true ]; then
        speedtest
    elif [ "$download" = true ]; then
        speedtest --no-upload
    elif [ "$upload" = true ]; then
        speedtest --no-download
    fi
done
