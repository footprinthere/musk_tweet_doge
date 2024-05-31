from typing import Optional
from datetime import datetime, timedelta

from tqdm import tqdm

from .aggregator import Aggregator
from .tools import single_import_returns
from data.price import get_price_data


class PriceAggregator(Aggregator):

    def __init__(self):
        super().__init__()
        self._column_name = "DOGEUSDT"

    def use_column(self, column_name: str) -> None:
        self._column_name = column_name

    def create_multiple_events(
        self,
        *,
        event_times: list[datetime],
        data_files: Optional[list[str]] = None,
        data_time_delta: Optional[timedelta] = None,
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        result_file_format: Optional[str] = None,
    ) -> None:
        """
        * Either `data_files` or `data_time_delta` should be specified
        * `result_file_format` : str that includes a format `{}` to be replaced by the index of the `event_time`
        """
        if result_file_format is not None:
            if "{}" not in result_file_format:
                raise ValueError("`result_file_format` should include a format `{}`")

        if data_files is not None:
            print("Using saved dataset files")
            for idx, (event_time, data_file) in enumerate(
                tqdm(list(zip(event_times, data_files)))
            ):
                self.create_event(
                    data_file=data_file,
                    column_name=self._column_name,
                    is_price=True,
                    event_time=event_time,
                    event_window=event_window,
                    estimation_window=estimation_window,
                    result_file=(
                        None
                        if result_file_format is None
                        else result_file_format.format(idx)
                    ),
                )
            return

        if data_time_delta is None:
            raise ValueError(
                "Either `data_files` or `data_time_delta` should be specified"
            )

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
        data_save_path: Optional[str] = None,
        result_file: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
        Aggregator._validate_window(event_window, estimation_window)

        data = get_price_data(
            start_time=event_time - data_time_delta,
            end_time=event_time + data_time_delta,
            file_path=data_save_path,
            verbose=verbose,
        )
        single_import_returns(
            data=data,
            is_price=True,
            log_return=True,
        )

        self._add_event(
            column_name=self._column_name,
            event_time=event_time,
            event_window=event_window,
            estimation_window=estimation_window,
            result_file=result_file,
        )
