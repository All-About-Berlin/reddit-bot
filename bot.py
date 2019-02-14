#!/usr/bin/python3
import praw
import os
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

filters = (
    (
        'messages/visiting.md',
        (
            'airport',
            'be in berlin',
            'coming to berlin',
            'first time',
            'flying to berlin',
            'going to berlin',
            'souvenir'
            'stay',
            'taxi',
            'touristy',
            'travel to',
            'traveller',
            'travelling to',
            'trip',
            'visiting',
            'welcome card',
            'will be in berlin',
            'stag ',
        )
    ),
    (
        'messages/moving.md',
        (
            'move to',
            'moving to',
            'relocating to',
        )

    ),
    (
        'messages/nightlife.md',
        (
            'bars',
            'berghain',
            'cassiopeia',
            'clubbing',
            'clubs',
            'griessmuehle',
            'griesmuehle',
            'live music',
            'matrix',
            'nightlife',
            'sisyphos'
            'tresor',
            'watergate',
            'kit kat',
            'kitkat',
        )
    ),
    (
        'messages/apartment.md',
        (
            'find an apartment',
            'find an flat',
        )
    ),
    (
        'messages/jobs.md',
        (
            'jobs',
            'salaries',
            'salary',
            'internship',
            'career',
            'find a job',
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
                with open(message_path, 'r') as message_file:
                    submission.reply(message_file.read())
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