from omegaconf import DictConfig
import pandas as pd
from typing import Dict, Iterator, Any
from data.tweet_processor import Tweet_Processor


def csv_data_generator(
    cfg: DictConfig, tweet_data_iterator: Iterator[Dict[str, Any]]
) -> pd.DataFrame:

    tweet_processor = Tweet_Processor(
        cfg.scraper.twitter_search_module_config.tweet_params_to_extract
    )
    processed_tweets = tweet_processor(tweet_data_iterator)
    return pd.DataFrame(processed_tweets)
