from typing import List, Iterator, Dict, Any, Optional


class Reddit_Processor(object):
    def __init__(self, reddit_params_to_extract: List[str]) -> None:
        self.fields_to_extract = reddit_params_to_extract
        self.field_value_processors = {
            "body": self.process_body,
        }

    def __call__(self, data_iterator: Iterator[Dict[str, Any]]):
        # TODO: Revisit this code to setup batched data collection when querying
        # large amount of Twitter data.
        all_reddit_dicts = []
        for current_data_dict, current_query in data_iterator():
            post_subset = self.extract_fields(current_data_dict)
            post_subset["query"] = current_query
            post_subset = self.process_fields(post_subset)
            if post_subset.get('body') and post_subset['body'].strip():
                all_reddit_dicts.append(post_subset)
        return all_reddit_dicts

    def process_fields(self, datapoint_subset: Dict[str, Any]):
        for current_field, current_value in datapoint_subset.items():
            if current_field in self.field_value_processors:
                current_value = self.field_value_processors[current_field](
                    current_value
                )
            datapoint_subset[current_field] = current_value
        return datapoint_subset

    def extract_fields(self, raw_datapoint: Dict[str, Any]):
        return {
            key: value
            for key, value in raw_datapoint.items()
            if key in self.fields_to_extract
        }

    def process_body(self, content: str):
        content = content.replace("\t", "")
        content = content.replace("\r", "")
        return content
