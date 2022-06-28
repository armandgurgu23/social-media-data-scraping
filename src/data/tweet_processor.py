from typing import List, Iterator, Dict, Any, Optional


class Tweet_Processor(object):
    def __init__(self, tweet_params_to_extract: List[str]) -> None:
        self.fields_to_extract = tweet_params_to_extract
        self.field_value_processors = {
            "hashtags": self.process_hashtags,
            "content": self.process_content,
        }

    def __call__(self, tweet_data_iterator: Iterator[Dict[str, Any]]):
        # TODO: Revisit this code to setup batched data collection when querying
        # large amount of Twitter data.
        all_tweet_dicts = []
        for current_tweet_dict, current_query in tweet_data_iterator():
            tweet_subset = self.extract_fields_from_tweet(current_tweet_dict)
            tweet_subset["query"] = current_query
            tweet_subset = self.process_fields(tweet_subset)
            if tweet_subset.get('content') and tweet_subset['content'].strip():
                all_tweet_dicts.append(tweet_subset)
        return all_tweet_dicts

    def extract_fields_from_tweet(self, raw_tweet: Dict[str, Any]):
        return {
            key: value
            for key, value in raw_tweet.items()
            if key in self.fields_to_extract
        }

    def process_fields(self, tweet_subset: Dict[str, Any]):
        for current_field, current_value in tweet_subset.items():
            if current_field in self.field_value_processors:
                current_value = self.field_value_processors[current_field](
                    current_value
                )
            tweet_subset[current_field] = current_value
        return tweet_subset

    def process_hashtags(self, hashtags: Optional[List[str]]):
        if hashtags:
            return "[HASH-SEP]".join(hashtags)
        else:
            return None

    def process_content(self, content: str):
        content = content.replace("\t", "")
        content = content.replace("\r", "")
        return content
