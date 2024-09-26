#!/bin/bash

echo "Get ready!!!"
echo "5..."
sleep 1
echo "4..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1

python3 ./rocket.py 2>rocket.err.csv | tee rocket.out | python3 ./keyboard.py
