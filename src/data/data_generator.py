from omegaconf import DictConfig
import pandas as pd
from typing import Dict, Iterator, Any
from data.tweet_processor import Tweet_Processor
from data.reddit_processor import Reddit_Processor


def csv_data_generator(
    cfg: DictConfig, data_iterator: Iterator[Dict[str, Any]]
) -> pd.DataFrame:

    if cfg.scraper.name == 'twitter':
        tweet_processor = Tweet_Processor(
            cfg.scraper.twitter_search_module_config.tweet_params_to_extract
        )
        processed_tweets = tweet_processor(data_iterator)
        return pd.DataFrame(processed_tweets)
    elif cfg.scraper.name == 'reddit':
        reddit_processor = Reddit_Processor(
            reddit_params_to_extract=cfg.scraper.subreddit_search_module_config.subreddit_params_to_extract)
        processed_posts = reddit_processor(data_iterator)
        return pd.DataFrame(processed_posts)
