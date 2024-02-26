# /r/berlin bot

Reddit bot for /r/berlin. This bot provides helpful answers to common questions and directs users to the sticky thread. Currently deactivated.

## Setup

1. Pull the repository and run `pip install -r requirements.txt`.
2. Create a `praw.ini` configuration file with the following content:
    ```
    [berlin-bot]
    client_id=reddit app ID
    client_secret=reddit app secret
    user_agent=/r/berlin Tourism bot
    password=...
    username=...
    ```
3. Run `python3 bot.py`
