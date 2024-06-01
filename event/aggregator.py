from typing import Optional
from datetime import datetime

import numpy as np
from pandas import DataFrame
from eventstudy import Single, Multiple
from eventstudy.excelExporter import write_Single, write_Multiple


class Aggregator:
    def __init__(self):
        self.events: list[Single] = []

    def reset(self) -> None:
        self.events.clear()

    def create_event(
        self,
        *,
        data_file: str,
        column_name: str,
        is_price: bool,
        event_time: datetime,
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        result_file: Optional[str] = None,
    ) -> None:
        Aggregator._validate_window(event_window, estimation_window)

        Single.import_returns(
            path=data_file,
            is_price=is_price,
            log_return=True,
            date_format="%Y-%m-%dT%H:%M:%S",
        )

        self._add_event(
            column_name=column_name,
            event_time=event_time,
            event_window=event_window,
            estimation_window=estimation_window,
            result_file=result_file,
        )

    def aggregate(
        self,
        result_file: str,
        asterisks: bool = True,
        rounding: int = 3,
    ) -> DataFrame:
        multiple = Multiple(self.events)
        write_Multiple(multiple, result_file)
        return multiple.results(asterisks=asterisks, decimals=rounding)

    def _add_event(
        self,
        column_name: str,
        event_time: datetime,
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
        result_file: Optional[str],
    ) -> None:
        event = Single.constant_mean(
            security_ticker=column_name,
            event_date=np.datetime64(event_time),
            event_window=event_window,
            estimation_size=estimation_window[1] - estimation_window[0],
            buffer_size=-1 * estimation_window[1],
        )
        self.events.append(event)

        if result_file is not None:
            write_Single(event, result_file)

    @staticmethod
    def _validate_window(
        event_window: tuple[int, int],
        estimation_window: tuple[int, int],
    ):
        if event_window[0] >= event_window[1]:
            raise ValueError("Event window start must be before end")
        if not estimation_window[0] < estimation_window[1] <= 0:
            raise ValueError("Estimation window must be negative")
