import requests
import json
import os

def fetch(nzbn, operation):
    """Fetches data from the API based on the provided nzbn and operation."""
    
    if not nzbn or not operation:
        raise ValueError("Both 'nzbn' and 'operation' must be provided.")

    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise ValueError("API key not set in environment variables!")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    url = f"https://api.business.govt.nz/gateway/nzbn/v5/entities/{nzbn}/{operation}/"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    try:
        formatted_response = json.dumps(response.json(), indent=4)
    except json.JSONDecodeError:
        raise ValueError("Failed to decode JSON response from API.")

    file_name = f"{operation}.json"

    with open(file_name, "w") as file:
        file.write(formatted_response)

    print(f"Data fetched successfully and saved to {file_name}")

if __name__ == "__main__":
    nzbn = 9429040077536
    operation = "filings"
    
    fetch(nzbn, operation)
