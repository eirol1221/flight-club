class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, fly_from_code, fly_from_city, fly_to_code, fly_to_city, price, flight_date_from, flight_date_to, stop_overs=0, via_city=""):
        self.fly_from_code = fly_from_code
        self.fly_from_city = fly_from_city
        self.fly_to_code = fly_to_code
        self.fly_to_city = fly_to_city
        self.price = price
        self.flight_date_from = flight_date_from
        self.flight_date_to = flight_date_to
        self.stop_overs = stop_overs
        self.via_city = via_city
