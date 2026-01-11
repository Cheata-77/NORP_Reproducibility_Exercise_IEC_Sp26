import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import sys

BASE_URL = "https://data.cityofchicago.org/resource/crimes.json"

API_ID = "d92ljy2mqk70m1z6hhnzr903u"
API_SECRET = "5rbj9ulsenffo38cn867oaqbk1h7qt140i50vm925ctuvwlmv8"
APP_TOKEN = "QkOfjqTOtyjSCKjNNfggkriKr"
APP_TOKEN_SECRET = "3_13j9wkyDgI_TKkYTkwlOkLKe7HYIFoc7zF"


def run_query(params, timeout=5):
    headers = {"X-App-Token": APP_TOKEN}
    auth = HTTPBasicAuth(API_ID, API_SECRET)

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            auth=auth,
            timeout=timeout,
        )
        
        # Print the final URL for debugging
        print("Request URL:", response.url)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

    if response.status_code == 200:
        try:
            data = response.json()   # top-level list of rows (dicts)
        except ValueError as e:
            print(f"JSON decode error: {e}")
            return None

        if not data:
            print("No data returned.")
            return None

        df = pd.DataFrame(data)
        print("Columns:", list(df.columns))
        print("Rows returned:", len(df))
        return df
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
if __name__ == "__main__":
    
    # Simple test
    
    params = {
        "$select": "primary_type, count(primary_type) as type_count",
        "$group": "primary_type",
        "$order": "type_count DESC",
        "$limit": "5"
    }   
    
    df = run_query(params)
    if df is not None:
        print(df)