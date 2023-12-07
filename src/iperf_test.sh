#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <название_файла>"
    exit 1
fi

iperf3 -c 192.168.0.101 -f m -p 8080 -t 30 -R > iperf_data.txt
python3 iperf_parser.py $1

echo "Данные сохранены в $1"
