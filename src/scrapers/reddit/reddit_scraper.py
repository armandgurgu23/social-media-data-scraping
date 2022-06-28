from omegaconf import DictConfig
import logging
from scrapers.reddit.subreddit.subreddit_scraper import Subreddit_Search_Handler
from data.data_generator import csv_data_generator
from os import getcwd


logger = logging.getLogger(__name__)


def main_reddit_scraper(cfg: DictConfig) -> None:
    logger.info("Running reddit scraper!")
    if cfg.scraper.scraper_module == "subreddit":
        data_handler = Subreddit_Search_Handler(
            cfg.scraper.subreddit_search_module_config)
        logger.info(
            f'Finished initializing the Reddit {cfg.scraper.scraper_module} module! Scraping will start!')
    else:
        raise NotImplementedError(
            f"Scraper module {cfg.scraper.scraper_module} not supported for Reddit!"
        )

    # Handle serializing the scraped data.
    output_path = f'{cfg.scraper.name}_{cfg.scraper.scraper_module}_datadump_{getcwd().split("/")[-1]}.{cfg.scraper.output_format}'

    if cfg.scraper.output_format == "csv":
        csv_data = csv_data_generator(cfg, data_handler)
        csv_data.to_csv(path_or_buf=output_path, **
                        cfg.scraper.pandas_to_csv_config)
    else:
        raise NotImplementedError(
            f"Outputting scraped dataset in format {cfg.scraper.output_format} not supported for Reddit!"
        )

    logger.info(
        f"Finished running Reddit scraper! Dataset dumped at: {getcwd()}")

    return
