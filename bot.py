#!/usr/bin/python3
import praw
import os
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

filters = (
    (
        'messages/drugs.md',
        (
            'weed',
            'cannabis',
            'marijuana',
            'mdma',
            'cocaine',
        )
    ),
    (
        'messages/taxnumber.md',
        (
            'rentenversicherungsnummer',
            'rnvr',
            'sozialversicherungsnummer',
            'steuer id',
            'steuer-id',
            'steuerid',
            'steueridentifikationsnummer',
            'steuernummer',
            'tax id',
            'tax id',
            'tax number',
            'tax number',
            'umsatzsteuernummer',
            'versicherungsnummer',
        )
    ),
    (
        'messages/friends.md',
        (
            'make friends',
            'lonely',
            'new friends',
            'loneliness',
            'meet new',
            'meet some',
        )
    ),
    (
        'messages/visa.md',
        (
            ' visa',
            'blue card',
            'residence permit',
        )
    ),
    (
        'messages/doctors.md',
        (
            'doctor',
            ' gp ',
            'gynecologist',
            'osteopath',
        )
    ),
    (
        'messages/healthinsurance.md',
        (
            'krankenkasse',
            'health insurance',
            'techniker krankenkasse',
            ' tk ',
            ' aok ',
        )
    ),
    (
        'messages/apartment.md',
        (
            'find an apartment',
            'find a flat',
            'find an room',
            'find an wg',
            'looking for an apartment',
            'looking for a room',
            'looking for a flat',
            'looking for a wg',
        )
    ),
    (
        'messages/jobs.md',
        (
            'jobs',
            'job market',
            'salaries',
            'salary',
            'internship',
            'career',
            'find a job',
        )
    ),
    (
        'messages/anmeldung.md',
        (
            'address registration',
            'anmeldung',
            'burgeramt',
            'bürgeramt',
            'register my',
            'ummeldung',
        )
    ),
    (
        'messages/moving.md',
        (
            'move to',
            'moving to',
            'relocate to',
            'relocating to',
        )
    ),
    (
        'messages/visiting.md',
        (
            'airport',
            'heading to berlin',
            'be in berlin',
            'coming to berlin',
            'the first time',
            'flying to berlin',
            'going to berlin',
            'hotel',
            'souvenir'
            'touristy',
            'travel to',
            'traveller',
            'traveler',
            'travelling to',
            'traveling to',
            'trip ',
            'visiting ',
            'welcome card',
            'will be in berlin',
            'stag ',
        )
    ),
    (
        'messages/nightlife.md',
        (
            'bars',
            'berghain',
            'cassiopeia',
            'club',
            'clubbing',
            'clubs',
            'griesmuehle',
            'griessmuehle',
            'kit kat',
            'kitkat',
            'live music',
            'matrix',
            'nightlife',
            'party',
            'sisyphos'
            'techno',
            'tresor',
            'watergate',
        )
    ),
    (
        'messages/english.md',
        (
            'english-speaking',
            'english speaking',
            'who speaks english',
            'who speak english',
        )
    ),
)


def get_processed_submissions():
    processed_submissions = []
    if os.path.isfile("replied_to.txt"):
        with open("replied_to.txt", "r") as f:
            processed_submissions = f.read().split("\n")
            processed_submissions = list(filter(None, processed_submissions))
    return processed_submissions


def is_upvoted(submission):
    """
    If a comment is upvoted, we assume the question is welcomed, and that
    there's no need for a template answer.
    """
    min_score = 3
    min_comment_count = 1
    return (
        submission.score > min_score and
        len(submission.comments) > min_comment_count
    )


def has_keywords(submission, keywords):
    return (
        any(kw in submission.title.lower() for kw in keywords) or
        any(kw in submission.selftext.lower() for kw in keywords)
    )


def police_subreddit(subreddit, limit=20):
    """Reply to posts that match the given keywords"""
    reddit = praw.Reddit('berlin-bot')
    processed_submissions = get_processed_submissions()
    for submission in reddit.subreddit(subreddit).new(limit=limit):
        if submission.id in processed_submissions:
            logger.info('Post "{}" ({}) was already replied to.'.format(submission.title, submission.id))
            continue

        for message_path, trigger_keywords in filters:
            if has_keywords(submission, trigger_keywords) and not is_upvoted(submission):
                logger.info('Replying to "{}" ({}) with {}'.format(
                    submission.title, submission.id, message_path
                ))
                with open(message_path, 'r') as message_file, open('messages/footer.md', 'r') as footer_file:
                    submission.reply(message_file.read() + footer_file.read())
                with open("replied_to.txt", "a") as replied_to_file:
                    replied_to_file.write(submission.id + "\n")
                break


def police_self(username, limit=20, minimum_score=-1):
    """Delete own comments if they are below a certain score."""
    reddit = praw.Reddit('berlin-bot')
    bot = reddit.redditor('berlin-bot')
    for comment in bot.comments.new(limit=limit):
        if comment.score <= minimum_score:
            logger.info('Removing own comment on "{}" due to low score'.format(
                comment.parent().title
            ))
            comment.delete()


police_subreddit('berlin')
police_self('berlin-bot')
