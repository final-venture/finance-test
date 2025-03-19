import requests
import json
import os
import re
from datetime import datetime

def get(nzbn, operation):
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
        data = response.json()
        formatted_response = json.dumps(data, indent=4)
    except json.JSONDecodeError:
        raise ValueError("Failed to decode JSON response from API.")

    file_name = f"{operation}.json"
    with open(file_name, "w") as file:
        file.write(formatted_response)

    print(f"Data fetched successfully and saved to {file_name}")
    return data

def get_all_filings(nzbn):
    return get(nzbn, "filings")

def fetch_filing_attachments(filing, nzbn, base_dir="downloads"):
    """Downloads attachments for a given filing and saves it to a directory named after nzbn."""
    if not filing.get("attachments"):
        print(f"No attachments for filing {filing['filingId']}")
        return

    filing_dir = os.path.join(base_dir, str(nzbn))
    os.makedirs(filing_dir, exist_ok=True)

    # Parse the registrationDate to extract the year
    registration_date = filing["registrationDate"]
    year = datetime.strptime(registration_date, "%Y-%m-%dT%H:%M:%S.%f%z").year

    for attachment in filing["attachments"]:
        doc_id = attachment["documentId"]
        doc_url = attachment["document"]["href"]

        # Use the year as the filename
        file_path = os.path.join(filing_dir, f"{year}.pdf")
        
        if os.path.exists(file_path):
            print(f"File {file_path} already exists. Skipping download.")
            continue

        response = requests.get(doc_url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded attachment {doc_id} to {file_path}")
        else:
            print(f"Failed to download {doc_id}: Status {response.status_code}")

def fetch_all_returns(nzbn):
    """Downloads All Annual Returns."""
    data = get_all_filings(nzbn)
    if "items" not in data:
        raise ValueError("No 'items' key found in the data.")

    pattern = r".*ACCFIN.*"
    regex = re.compile(pattern)

    for item in data["items"]:
        filing_code = item["filingCode"]
        if regex.match(filing_code):
            print(f"Match found: {filing_code} (Filing ID: {item['filingId']})")
            fetch_filing_attachments(item, nzbn)
        else:
            print(f"No match: {filing_code} (Filing ID: {item['filingId']})")

if __name__ == "__main__":
    nzbn = 9429040077536
    fetch_all_returns(nzbn)

# TODO: Dynamic Sync
