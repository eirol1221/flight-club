import requests
from flight_data import FlightData
import os
from pprint import pprint

TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def search_flights(self, fly_to, fly_from, date_from, date_to):
        header = {
            "apikey": TEQUILA_API_KEY,
            "accept": "application/json"
        }

        parameters = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "one_for_city": 1,
            "max_stopovers": 0,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "GBP",
        }

        response = requests.get(url="https://api.tequila.kiwi.com/search",
                                headers=header,
                                params=parameters)

        try:
            data_flight = response.json()["data"][0]
        except IndexError:
            parameters["max_stopovers"] = 1
            response = requests.get(url="https://api.tequila.kiwi.com/search",
                                headers=header,
                                params=parameters)
            try:
                data_flight = response.json()["data"][0]
            except IndexError:
                print(f"No flights found for {fly_to}")
                return None
            else:
                pprint(data_flight)

                flight_data = FlightData(
                    fly_from_code=data_flight["route"][0]["flyFrom"],
                    fly_from_city=data_flight["route"][0]["cityFrom"],
                    fly_to_code=data_flight["route"][0]["flyTo"],
                    fly_to_city=data_flight["route"][0]["cityTo"],
                    price=data_flight["price"],
                    flight_date_from=data_flight["route"][0]["dTime"],
                    flight_date_to=data_flight["route"][0]["aTime"],
                    stop_overs=1,
                    via_city=data_flight["route"][0]["cityTo"]
                )

                return flight_data
        else:
            flight_data = FlightData(
                fly_from_code=data_flight["route"][0]["flyFrom"],
                fly_from_city=data_flight["route"][0]["cityFrom"],
                fly_to_code=data_flight["route"][0]["flyTo"],
                fly_to_city=data_flight["route"][0]["cityTo"],
                price=data_flight["price"],
                flight_date_from=data_flight["route"][0]["dTime"],
                flight_date_to=data_flight["route"][0]["aTime"]
            )

            return flight_data

    def get_IATA_codes(self, city):
        headers = {
            "apikey": TEQUILA_API_KEY
        }

        parameters = {
            "term": city
        }

        response = requests.get(url="https://api.tequila.kiwi.com/locations/query",
                                params=parameters, headers=headers)
        return response.json()['locations'][0]['code']

