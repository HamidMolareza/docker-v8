#!/bin/bash

date_time_file="date.txt"
rm "$date_time_file"

date >> "$date_time_file"

docker build -t d8 .

date >> "$date_time_file"