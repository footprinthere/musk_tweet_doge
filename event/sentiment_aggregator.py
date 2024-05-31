from typing import Optional
from datetime import datetime

from tqdm import tqdm

from event.aggregator import Aggregator


class SentimentAggregator(Aggregator):

    def __init__(self):
        super().__init__()
        self._column_name = ""

    def use_column(self, column_name: str) -> None:
        self._column_name = column_name

    def create_multiple_events(
        self,
        *,
        event_times: list[datetime],
        data_files: list[str],
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        result_file_format: Optional[str] = None,
    ) -> None:
        if result_file_format is not None:
            if "{}" not in result_file_format:
                raise ValueError("`result_file_format` should include a format `{}`")

        for idx, (event_time, data_file) in enumerate(
            tqdm(list(zip(event_times, data_files)))
        ):
            self.create_event(
                data_file=data_file,
                column_name=self._column_name,
                is_price=False,  # Specified column must include calculated returns
                event_time=event_time,
                event_window=event_window,
                estimation_window=estimation_window,
                result_file=(
                    None
                    if result_file_format is None
                    else result_file_format.format(idx)
                ),
            )
