from typing import Any, Dict, List
import tweepy
from src.connection import trends_collection
from src.config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def _get_user_timeline_tweets(username: str, api: tweepy.API) -> List[Dict[str, Any]]:
    """Get tweets from a user's timeline using Twitter API v1.1.

    Args:
        username (str): Twitter username.

    Returns:
        List[Dict[str, Any]]: Tweets list.
    """
    tweets = api.user_timeline(screen_name=username, count=10)
    return [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets]

def get_tweets() -> List[Dict[str, Any]]:
    """Get tweets persisted in MongoDB.

    Returns:
        List[Dict[str, Any]]: Tweets list.
    """
    tweets = trends_collection.find({})
    return list(tweets)

def save_tweets() -> None:
    """Get tweets and save on MongoDB."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    tweets = _get_user_timeline_tweets(username="TwitterDev", api=api)
    trends_collection.insert_many(tweets)
