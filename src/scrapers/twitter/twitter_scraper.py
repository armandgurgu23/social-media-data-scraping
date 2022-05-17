from omegaconf import DictConfig
import logging
from scrapers.twitter.queries.search.twitter_search_scraper import (
    Twitter_Search_Handler,
)
from data.data_generator import csv_data_generator
from os import getcwd

logger = logging.getLogger(__name__)


def main_twitter_scraper(cfg: DictConfig) -> None:
    logger.info("Running twitter scraper!")
    if cfg.scraper.scraper_module == "search":
        data_handler = Twitter_Search_Handler(cfg.scraper.twitter_search_module_config)
    else:
        raise NotImplementedError(
            f"Scraper module {cfg.scraper.scraper_module} not supported for Twitter!"
        )

    # Handle serializing the scraped data.
    output_path = f'{cfg.scraper.name}_{cfg.scraper.scraper_module}_datadump_{getcwd().split("/")[-1]}.{cfg.scraper.output_format}'

    if cfg.scraper.output_format == "csv":
        csv_data = csv_data_generator(cfg, data_handler)
        csv_data.to_csv(path_or_buf=output_path, **cfg.scraper.pandas_to_csv_config)
    else:
        raise NotImplementedError(
            f"Outputting scraped dataset in format {cfg.scraper.output_format} not supported for Twitter!"
        )

    logger.info(f"Finished running twitter scraper! Dataset dumped at: {getcwd()}")

    return
