# RM - RapMachine

## Use

 - Run `python BotScript.py` for the Tweetbot
 - Run `python src/test_generation.py` with proper parameters to test language generation. 


## Installation

- Create an `.env` file including the variables:
    - `CONSUMER_API_KEY`
    - `CONSUMER_API_KEY_SECRET`
    - `ACCESS_TOKEN`
    - `ACCESS_TOKEN_SECRET`
    and provide the needed credentials to each variable.
- Install requirements `pip install -r requirements.txt`


## Prerequisites

- Apply for a [Twitter Developer Account with elevated access](https://developer.twitter.com/en)
- Download [fasttext's language identification model](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin) and 
  place it in the same folder as this file.
- Create a folder called `.model` in the same folder as this file and place the proper finetuned GPT-2 model inside it 
  (`.model/GPT-2-finetuned/config.json pytorch...`). The model is available [here](https://drive.google.com/drive/folders/116WlytHENvyNia_xZr7GxUEym20SjeQn?usp=sharing)
- Hardware that can deal with GPT-2.


## Data Documentation
 
- We gathered raps from genius.com, ohhla.com and battlerap.com. For genius.com, we used the official [API](https://docs.genius.com/) 
  (GeniusLyrics and GetRankings repos) while genius.com and ohhla.com were scraped using a specifically tailored scrapy scraper.
  In total we gathered ~70k raps which we used for finetuning. GPT-2 was finetuned by creating one large text, while T5 was finetuned
  on prompts. The prompts had the form of `KEYWORDS: <keywords> RAP-LYRICS: <rap text>` which proved to be insufficient for our task.