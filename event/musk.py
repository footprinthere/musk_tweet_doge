from datetime import datetime, timedelta


MUSK_TWEET_TIMES = [
    datetime(2021, 1, 28, 23, 47, 0),  # 7
    datetime(2021, 2, 4, 8, 35, 0),  # 9
    datetime(2021, 2, 6, 5, 2, 0),  # 10
    datetime(2021, 2, 7, 8, 41, 0),  # 11
    datetime(2021, 2, 7, 23, 25, 0),  # 12
    datetime(2021, 2, 10, 16, 8, 0),  # 14
    datetime(2021, 2, 11, 10, 8, 0),  # 15
    datetime(2021, 2, 15, 0, 25, 0),  # 16 - requires 2-day data
    datetime(2021, 2, 21, 22, 27, 0),  # 18
    datetime(2021, 2, 24, 14, 0, 0),  # 19
    datetime(2021, 3, 1, 20, 57, 0),  # 20
    datetime(2021, 3, 6, 5, 40, 0),  # 22
    datetime(2021, 3, 14, 0, 40, 0),  # 24 - requires 2-day data
    datetime(2021, 4, 1, 12, 25, 0),  # 26
    datetime(2021, 4, 9, 9, 32, 0),  # 27
    datetime(2021, 4, 15, 5, 33, 0),  # 28 - Ante said "6:33:00", but looks like a typo
    datetime(2021, 4, 16, 19, 1, 0),  # 29
    datetime(2021, 4, 28, 8, 20, 0),  # 30
]

# Revise timezone to GMT
timezone_delta = timedelta(hours=-1)
MUSK_TWEET_TIMES = [time + timezone_delta for time in MUSK_TWEET_TIMES]


if __name__ == "__main__":
    print(len(MUSK_TWEET_TIMES))
    print(*MUSK_TWEET_TIMES, sep="\n")
