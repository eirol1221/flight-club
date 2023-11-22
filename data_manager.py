import requests
import os

SHEETY_PRICES_URL = os.environ["SHEETY_PRICES_URL"]
SHEETY_USERS_URL = os.environ["SHEETY_USERS_URL"]


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def add_user(self, fname, lname, email):
        body = {
            "user": {
                "firstName": fname,
                "lastName": lname,
                "email": email,
            }
        }
        response = requests.post(url=SHEETY_USERS_URL, json=body)

    def get_user_email(self):
        response = requests.get(url=SHEETY_USERS_URL)
        user_emails = []
        for user in response.json()["users"]:
            user_emails.append(user['email'])
        return user_emails

    def get_data(self):
        response = requests.get(url=SHEETY_PRICES_URL)
        return response.json()['prices']

    def update_iata(self, iata_code, id):
        body = {
            "price": {
                "iataCode": iata_code
            }
        }

        response = requests.put(url=f"{SHEETY_PRICES_URL}/{id}",
                                json=body)
        print(response.text)