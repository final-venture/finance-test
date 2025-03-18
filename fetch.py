import requests
import json
import os

def fetch(nzbn=None, operation=None):
    """Fetches data from the API based on the provided nzbn and operation."""
    api_key = os.getenv("API_KEY")

    if api_key is None:
        raise ValueError("API key not set in environment variables!")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    if nzbn is None:
        nzbn = input("Enter NZBN: ")
    if operation is None:
        operation = input("Enter Operation: ")

    url = f"https://api.business.govt.nz/gateway/nzbn/v5/entities/{nzbn}/{operation}/"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise ValueError(f"Request failed with status code {r.status_code}")

    formatted_response = json.dumps(r.json(), indent=4)

    with open(f"{operation}.json", "w") as file:
        file.write(formatted_response)

    print(f"Data fetched successfully and saved to {operation}.json")

if __name__ == "__main__":
    fetch()
