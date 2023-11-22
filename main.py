# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.

from flight_search import FlightSearch
from notification_manager import NotificationManager
from data_manager import DataManager
from datetime import *
from dateutil.relativedelta import *

data_manager = DataManager()
notification_manager = NotificationManager()
flight_search = FlightSearch()

# -------------- ADD FLIGHT CLUB MEMBERS -------------- #
print("Welcome to Lorie's Flight Club.\nWe find the best flight deals and email you.")
first_name = input("What is your first name?\n").title()
last_name = input("What is your last name?\n").title()

email_matched = False
while not email_matched:
    email = input("What is your email?\n").lower()
    email_retype = input("Type your email again.\n").lower()
    if email == email_retype:
        print("You're in the club!")
        data_manager.add_user(first_name, last_name, email)
        email_matched = True
    else:
        print("Email did not match. Try again.")

# -------------- GET IATA CODES -------------- #
sheet_data = data_manager.get_data()

for data in sheet_data:
    iata_code = data["iataCode"]
    if iata_code == "":
        iata_code = flight_search.get_IATA_codes(data['city'])
        data_manager.update_iata(iata_code, data["id"])


# -------------- SEARCH FOR AVAILABLE FLIGHTS -------------- #
date_from = datetime.now() + timedelta(days=1)
date_to = datetime.now() + relativedelta(months=6)
FLY_FROM = "LON"

for data in sheet_data:
    flight = flight_search.search_flights(
        data["iataCode"],
        FLY_FROM,
        date_from,
        date_to
    )

    if flight is not None and flight.price < data["lowestPrice"]:
        message = f"Subject: Lower price alert!\n\nOnly £{flight.price} to fly from {flight.fly_from_city}-{flight.fly_from_code} to {flight.fly_to_city}-{flight.fly_to_code}, from {datetime.fromtimestamp(flight.flight_date_from).strftime("%Y-%m-%d")} to {datetime.fromtimestamp(flight.flight_date_to).strftime("%Y-%m-%d")}"

        if flight.stop_overs > 0:
            message += f"\n\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            # print(message)

        notification_manager.send_mail(message, data_manager.get_user_email())
