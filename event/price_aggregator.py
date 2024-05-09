from typing import Optional
from datetime import datetime, timedelta

from tqdm import tqdm

from .aggregator import Aggregator
from .tools import single_import_returns
from data.price import get_price_data


class PriceAggregator(Aggregator):

    def create_multiple_price_events(
        self,
        *,
        event_times: list[datetime],
        data_time_delta: timedelta,
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        result_file_format: Optional[str] = None,
    ):
        """
        * `result_file_format` : str that includes a format `{}` to be replaced by the index of the event_time
        """
        if result_file_format is not None:
            if "{}" not in result_file_format:
                raise ValueError("result_file_format should include a format `{}`")

        for idx, event_time in enumerate(tqdm(event_times)):
            self.create_price_event(
                event_time=event_time,
                data_time_delta=data_time_delta,
                event_window=event_window,
                estimation_window=estimation_window,
                result_file=(
                    None
                    if result_file_format is None
                    else result_file_format.format(idx)
                ),
            )

    def create_price_event(
        self,
        *,
        event_time: datetime,
        data_time_delta: timedelta,
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        data_file: Optional[str] = None,  # save data as file
        result_file: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
        Aggregator._validate_window(event_window, estimation_window)

        data = get_price_data(
            start_time=event_time - data_time_delta,
            end_time=event_time + data_time_delta,
            file_path=data_file,
            verbose=verbose,
        )
        single_import_returns(
            data=data,
            is_price=True,
            log_return=True,
        )

        self._add_event(
            column_name="DOGEUSDT",
            event_time=event_time,
            event_window=event_window,
            estimation_window=estimation_window,
            result_file=result_file,
        )
