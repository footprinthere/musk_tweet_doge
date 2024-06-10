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

# Include all DOGE events in Ante
MUSK_TWEET_TIMES += [
    datetime(2020, 1, 10, 7, 53, 0),  # 3
    datetime(2020, 12, 20, 10, 30, 0),  # 5
    datetime(2020, 12, 25, 17, 47, 0),  # 6
    datetime(2021, 5, 7, 18, 24, 0),  # 31
    datetime(2021, 5, 10, 0, 41, 0),  # 32
    datetime(2021, 5, 11, 10, 13, 0),  # 33
    datetime(2021, 5, 14, 0, 45, 0),  # 36
    datetime(2021, 5, 20, 12, 41, 0),  # 38
    datetime(2021, 5, 24, 21, 49, 0),  # 40
    datetime(2021, 6, 2, 9, 5, 0),  # 41
    datetime(2021, 6, 25, 4, 10, 0),  # 43
    datetime(2021, 6, 25, 13, 3, 0),  # 44
    datetime(2021, 7, 1, 10, 43, 0),  # 45
    datetime(2021, 7, 2, 15, 20, 0),  # 46
    datetime(2021, 7, 25, 6, 23, 0),  # 47
]

# Revise timezone to GMT
timezone_delta = timedelta(hours=-1)
MUSK_TWEET_TIMES = [time + timezone_delta for time in MUSK_TWEET_TIMES]


if __name__ == "__main__":
    print(len(MUSK_TWEET_TIMES))
    print(*MUSK_TWEET_TIMES, sep="\n")
