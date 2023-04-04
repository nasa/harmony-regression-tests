#!/bin/bash

# removes any images downloaded by the test-in-bamboo.sh script.
# test-in-bamboo.sh writes to pulled-images.txt

while read -r line
do
    echo "removing $line"
    docker rmi "$line"
done < pulled-images.txt
