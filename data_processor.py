import re

import numpy as np
import pandas as pd

RAW_DATA_PATH = 'data/raw/'
FILENAME = 'five_connections_log.txt'
DATA_PATH = RAW_DATA_PATH + FILENAME

REQUEST_ID_PATTERN = r'Request ID (\d+)'
ACTION_PATTERN = r'\d+ (.*?) at time'
TIMESTAMP_PATTERN = r'at time (\d+)'

request_ids = np.array([], dtype=int) # store all request ids in the order they appear in the log as ints
actions = np.array([], dtype=str)
timestamps = np.array([], dtype=int)

with open(DATA_PATH, 'r') as file:
    for line in file:
        # capture all of the request ids in the order they appear in the log
        id = re.search(REQUEST_ID_PATTERN, line)
        request_ids = np.append(request_ids, int(id.group(1))) # type: ignore

        action = re.search(ACTION_PATTERN, line)
        actions = np.append(actions, action.group(1)) # type: ignore

        # capture all of the timestamps in the order they appear in the log
        timestamp = re.search(TIMESTAMP_PATTERN, line)
        timestamps = np.append(timestamps, int(timestamp.group(1))) # type: ignore