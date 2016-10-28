from __future__ import division
import datetime

def process_record(action, record):
    today = datetime.date.today()
    diff = today - record.date_posted
    number_month_since_posted = int(diff.days/30) + 1
    sqft_non_covered = record.sqft_lot - record.sqft_house
    # may need to remove int here
    result = 0
    if action == "spaciousness":
        spaciousness = (record.sqft_house / ((record.beds * 200 + record.baths * 100) + 400))
        result = int(record.price / spaciousness)
    else:
        result = int(
        (1/number_month_since_posted) *
        (record.price/(sqft_non_covered + 3/5 * record.sqft_house * record.condition)))
    return result, record.id


