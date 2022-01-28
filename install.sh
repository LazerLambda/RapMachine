#!/bin/bash

echo "CONSUMER_API_KEY=\nCONSUMER_API_KEY_SECRET=\nBEARER_TOKEN=\nACCESS_TOKEN=\nACCESS_TOKEN_SECRET=" > test.env
echo "Empty .env file created. Please provide necessary credentials: https://developer.twitter.com/en"

mkdir .model
echo "Empty .model folder created. Please download and extract the model from https://drive.google.com/drive/folders/116WlytHENvyNia_xZr7GxUEym20SjeQn?usp=sharing"

wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

pip install -r requirements.txt

