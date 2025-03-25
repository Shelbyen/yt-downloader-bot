# yt-downloader-bot
***yt downloader*** is a [*Telegram Bot*](https://core.telegram.org/bots) to download videos from [*YouTube*](https://www.youtube.com/).

# Requirements
You will need `FFmpeg` and `python >= 3.10`

# Setup
For set up the ***yt-downloader-bot***:

## Clone
Clone it to any place on your machine:
```bash
git clone https://github.com/Shelbyen/yt-downloader-bot.git
```
## Install requirements
```bash
pip install -r requirements.txt
```

## Set the environment variables
Create A file with name `.env` in the root of project. And fill it in as shown below:
```bash
TOKEN=<token> # (REQUIRED to be filled) your telegram bot token, detail here: https://core.telegram.org/bots/features#botfather
VERSION=<bot_version> # version of this project. Its only used in a logging, so you can leave it blank(but this field is REQUIRED)
DOWNLOADER=<downloader_name> # downloader name. Select or register your in DownloadersEnum
ADMINS=<first_admin>/<second_admin> # ids of admins of your bot. you can get it here: https://t.me/getmyid_bot
```
> [!Note]
> **All fields must be present, but not all must be filled in.**

> [!Note]
> *You can add more admins using `/` as divider*

# Using
And now you can just run it
```bash
python bot.py
```
