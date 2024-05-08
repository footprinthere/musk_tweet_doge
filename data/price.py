from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass

import pandas as pd
from tqdm import tqdm
from binance import Client


def get_price_data(
    symbol: str = "DOGEUSDT",
    *,
    start_time: datetime,
    end_time: datetime,
    interval: str = "1m",
    verbose: bool = False,
    file_path: Optional[str] = None,
) -> pd.DataFrame:

    data = get_kline_data(
        symbol=symbol,
        start_time=start_time,
        end_time=end_time,
        interval=interval,
        verbose=verbose,
    )

    df: list[dict[str, Any]] = []
    for entry in data:
        df.append(
            {
                "date": entry.open_time.strftime("%Y-%m-%d %H:%M:%S"),
                f"{symbol}": entry.open_price,
            }
        )

    pd_df = pd.DataFrame(df)
    if file_path is not None:
        pd_df.to_csv(file_path, index=False)

    return pd_df


def get_kline_data(
    symbol: str = "DOGEUSDT",
    *,
    start_time: datetime,
    end_time: datetime,
    interval: str = "1m",
    verbose: bool = False,
) -> list["KlineEntry"]:

    result: list[KlineEntry] = []
    progress = tqdm() if verbose else None

    call_start_time = start_time
    while call_start_time < end_time:
        result += _call_kline_api(
            symbol=symbol,
            start_time=call_start_time,
            end_time=end_time,
            interval=interval,
        )
        call_start_time = result[-1].close_time

        if progress is not None:
            progress.update(len(result))
            tqdm.write(f"last time: {call_start_time}")

    return result


def _call_kline_api(
    symbol: str = "DOGEUSDT",
    *,
    start_time: datetime,
    end_time: datetime,
    interval: str = "1m",
    limit: int = 1000,
) -> list["KlineEntry"]:

    response = Client().get_klines(
        symbol=symbol,
        interval=interval,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        limit=limit,
    )
    return [KlineEntry(*entry) for entry in response]


@dataclass
class KlineEntry:
    open_time: datetime
    open_price: float
    high_price: float
    low_price: float
    end_price: float
    volume: float
    close_time: datetime
    asset_volume: float
    n_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    _: str  # ignore

    def __post_init__(self):
        STR_TO_FLOAT = [
            "open_price",
            "high_price",
            "low_price",
            "end_price",
            "volume",
            "asset_volume",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
        ]
        for attr in STR_TO_FLOAT:
            setattr(self, attr, float(getattr(self, attr)))

        self.open_time = datetime.fromtimestamp(self.open_time / 1000)
        self.close_time = datetime.fromtimestamp(self.close_time / 1000)


if __name__ == "__main__":
    # Test
    start_time = datetime(2021, 1, 1)
    end_time = datetime(2021, 1, 5)
    data = get_kline_data(start_time=start_time, end_time=end_time, verbose=True)
    print(data[0])
    print(data[10])
    print(data[100])
    print(data[-1])
