from omegaconf import DictConfig
import logging
from scrapers.twitter.queries.search.twitter_search_scraper import (
    Twitter_Search_Handler,
)

logger = logging.getLogger(__name__)


def main_twitter_scraper(cfg: DictConfig) -> None:
    logger.info("Running twitter scraper!")
    if cfg.scraper.scraper_module == "search":
        twitter_search_handler = Twitter_Search_Handler(
            cfg.scraper.twitter_search_module_config
        )
        for current_tweet_dict, current_query in twitter_search_handler():
            print(current_tweet_dict)
            print(current_query)
        return
    else:
        raise NotImplementedError(
            f"Scraper module {cfg.scraper.scraper_module} not supported for Twitter!"
        )
