from zerver.lib.timestamp import ceiling_to_hour, ceiling_to_day, timestamp_to_datetime
from analytics.lib.counts import CountStat

from datetime import datetime, timedelta
from typing import List, Optional

# If min_length is None, returns end_times from ceiling(start) to ceiling(end), inclusive.
# If min_length is greater than 0, pads the list to the left.
# So informally, time_range(Sep 20, Sep 22, day, None) returns [Sep 20, Sep 21, Sep 22],
# and time_range(Sep 20, Sep 22, day, 5) returns [Sep 18, Sep 19, Sep 20, Sep 21, Sep 22]
def time_range(start, end, interval, min_length):
    # type: (datetime, datetime, str, Optional[int]) -> List[datetime]
    if interval == CountStat.HOUR:
        end = ceiling_to_hour(end)
        step = timedelta(hours=1)
    elif interval == CountStat.DAY:
        end = ceiling_to_day(end)
        step = timedelta(days=1)
    else:
        raise ValueError(_("Unknown interval."))

    times = []
    if min_length is not None:
        start = min(start, end - (min_length-1)*step)
    current = end
    while current >= start:
        times.append(current)
        current -= step
    return list(reversed(times))
