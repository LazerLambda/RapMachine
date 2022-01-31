# RM - RapMachine

## Use

 - Run `python BotScript.py` for the Tweetbot (This script runs only with `GPT2-rap-recommended`)
 - Run `python src/test_generation.py` with proper parameters to test language generation. 
 - To quit the program use `CTRL` + `C` 


## Installation

- Install requirements `pip install -r requirements.txt`
- Alternatively run `./install.sh`


## Prerequisites

- Apply for a [Twitter Developer Account with elevated access](https://developer.twitter.com/en)
- Create an `.env` file including the variables:
    - `CONSUMER_API_KEY`
    - `CONSUMER_API_KEY_SECRET`
    - `ACCESS_TOKEN`
    - `ACCESS_TOKEN_SECRET`
    and provide the necessary credentials to each variable.
- Download [fasttext's language identification model](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin) and 
  place it in the same folder as this file.
- Create a folder called `.model` in the same folder as this file and place the proper finetuned GPT-2 model (see Models section) inside it 
  (`.model/GPT2-rap-recommended/config.json pytorch...`). The model is available [here](https://drive.google.com/drive/folders/116WlytHENvyNia_xZr7GxUEym20SjeQn?usp=sharing)
- Hardware that can deal with GPT-2.


## Data Documentation
 
- We gathered raps from genius.com, ohhla.com and battlerap.com. For genius.com, we used the official [API](https://docs.genius.com/) 
  (GeniusLyrics and GetRankings repos) while genius.com and ohhla.com were scraped using a specifically tailored scrapy scraper.
  In total we gathered ~70k raps which we used for finetuning. GPT-2 was finetuned by creating one large text, while T5 was finetuned
  on prompts. The prompts had the form of `KEYWORDS: <keywords> RAP-LYRICS: <rap text>` which proved to be insufficient for our task.
  Eventually we chosed to use the fine-tuned GPT2 model. Experimental and succeeding scripts can be found in `./preprocessing/finetunging`. A short description can be
  found [here](https://github.com/LazerLambda/RapMachine/blob/master/preprocessing/DATADOC.md)

## Models
 - GPT2-rap-recommended [Download](https://drive.google.com/drive/folders/1zl_Zn7hUzsnr7FpdtV9VBo3SmmvM4jQO?usp=sharing) (Necessary to use BotScript.py)
 - GPT2-small-key2text [Download](https://drive.google.com/drive/folders/1FOrFDQgpnnBcSbXfGsBG2RkrjzggEaqx?usp=sharing) (Approach did not work, trained on 4k corpus)
 - T5-large-key2text [Download](https://drive.google.com/drive/folders/1dIsp7LmHwRXng8GX2fs__4JYrjpk-W4D?usp=sharing) (Approach did not work, trained on 70k corpus)
 - T5-small-key2text [Download](https://drive.google.com/drive/folders/1KyxvhLMDG2z1gCQ9aCSm4TmIL5CXq8Nz?usp=sharing) (Approach did not work, trained on 4k corpus)