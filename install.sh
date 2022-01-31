#!/bin/bash

echo "CONSUMER_API_KEY=\nCONSUMER_API_KEY_SECRET=\nBEARER_TOKEN=\nACCESS_TOKEN=\nACCESS_TOKEN_SECRET=" > test.env
echo "Empty .env file created. Please provide necessary credentials: https://developer.twitter.com/en"

mkdir .model
cd .model
mkdir GPT2-rap-recommended
cd ..
echo "Empty .model folder created. Please download and extract the model from https://drive.google.com/drive/folders/116WlytHENvyNia_xZr7GxUEym20SjeQn?usp=sharing"

FILE=lid.176.bin
if test -f "$FILE"; then
    echo "$FILE exist.\n"
else
    echo "$FILE does not exist. Download file.\n"
    wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
fi


pip install -r requirements.txt

