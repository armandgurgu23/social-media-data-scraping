from typing import Dict, List
import snscrape.modules.twitter as twitter_service
from omegaconf import DictConfig
from typing import Any, Iterator
from dataclasses import asdict


class Twitter_Search_Handler:
    def __init__(self, search_config: DictConfig) -> None:
        self.num_results_per_search = search_config.num_results_per_search
        self.search_queries_path = search_config.search_queries_path

    def __call__(self) -> Iterator[Dict[str, Any]]:
        # TODO: Figure out exact data structure of Tweet object.
        for current_query in self.queries_to_search:
            query_iterator = twitter_service.TwitterSearchScraper(
                current_query
            ).get_items()
            search_result_count = 0
            for current_result in query_iterator:
                search_result_count += 1
                if search_result_count == self.num_results_per_search:
                    break
                yield asdict(current_result), current_query

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
