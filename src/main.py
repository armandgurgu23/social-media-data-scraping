import hydra
from omegaconf import DictConfig
from scrapers.twitter.twitter_scraper import main_twitter_scraper


@hydra.main(config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    if cfg.scraper.name == "twitter":
        main_twitter_scraper(cfg)
    else:
        raise NotImplementedError(f"Scraper {cfg.scraper.name} not supported!")


if __name__ == "__main__":
    main()
