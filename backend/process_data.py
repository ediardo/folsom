import datetime
from __future__ import division

def process_record(action, record):
	record_id = record.id
	price = record.price
	sqft_house = record.sqft_house
	sqft_lot = record.sqft_lot
	condition = record.condition
	beds = record.beds
	baths = record.baths
	date_posted = record.date_posted
	today = datetime.date.today() 
	diff = today - date_posted
	number_month_since_posted = int(diff.days/30) + 1
	sqft_non_covered = sqft_lot - sqft_house
	# may need to remove int here
	house_quality_indicator = int((1/number_month_since_posted) * (price/(sqft_non_covered + 3/5 * sqft_house * condition)))
	spaciousness = ( sqft_house / ((beds * 200 + baths * 100) + 400))
	price_per_spaciousness = int( price / spaciousness )
	return [record_id, [house_quality_indicator,price_per_spaciousness]]


