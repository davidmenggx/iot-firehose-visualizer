import re

import numpy as np
import pandas as pd
import plotly.express as px

RAW_DATA_PATH = 'data/'
FILENAME = 'ten_connections_log.txt'
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

# normalize timestamps to all be in nanoseconds after first execution
normalized_timestamps = timestamps - timestamps[0]

# create ending timestamps with the start of the next event
ending_timestamps = normalized_timestamps[1:]
ending_timestamps = np.append(ending_timestamps, ending_timestamps[-1]) # for now I will have the last event be of length 0. A more accurate metric would be to calculate the program termination time

# calculate time delta for the amount of time each event is running
diffs = ending_timestamps - normalized_timestamps

# build a dataframe with the IDs, states, start time, end time, and time delta
data_dict = {'Id': request_ids, 'State': actions, 'Start': normalized_timestamps, 'End': ending_timestamps, 'Diff': diffs}
df = pd.DataFrame(data_dict)

# create a horizontal execution trace of the database actions
fig = px.bar(
    df, 
    x='Diff',
    y='Id',
    base='Start',
    orientation='h',
    color='State',
    labels={"Diff": "Duration (ns)", "Start": "Start Time (ns)"},
    title='Execution Trace of Database Actions'
)

fig.update_layout(
    xaxis_title='Time after execution (Nanoseconds)',
    yaxis_title='Request ID',
    xaxis=dict(tickformat=".0f")
)

fig.show()