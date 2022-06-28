from omegaconf import DictConfig
from typing import Iterator, Dict, Any, List
import snscrape.modules.reddit as reddit_service
from dataclasses import asdict


class Subreddit_Search_Handler:
    def __init__(self, search_config: DictConfig) -> None:
        self.num_results_per_search = search_config.num_results_per_search
        self.search_queries_path = search_config.search_queries_path

    def __call__(self) -> Iterator[Dict[str, Any]]:
        for current_query in self.queries_to_search:
            query_iterator = reddit_service.RedditSubredditScraper(
                current_query
            ).get_items()
            search_result_count = 0
            for current_result in query_iterator:
                if search_result_count == self.num_results_per_search:
                    break
                yield asdict(current_result), current_query
                search_result_count += 1

    @property
    def queries_to_search(self):
        return self.read_search_queries_from_path(self.search_queries_path)

    def read_search_queries_from_path(self, path: str) -> List[str]:
        search_queries = []
        with open(path, "r") as file_object:
            for current_query in file_object:
                current_query = current_query.replace("\n", "")
                search_queries.append(current_query)
        return search_queries
