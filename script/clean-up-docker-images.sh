#!/bin/bash

# removes any images downloaded by the test-in-bamboo.sh script.
# test-in-bamboo.sh writes to a pulled-images.txt, and we read that file here.

while read -r line
do
    echo "removing $line"
    docker rmi "$line"
done < pulled-images.txt
