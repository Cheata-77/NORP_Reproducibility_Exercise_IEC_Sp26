import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import ijson
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


def iter_dataset(json_path):
    with open(json_path, "rb") as f:
        # 'item' refers to each element of the top-level array
        for obj in ijson.items(f, "item"):
            yield obj


def run_dataset(json_path):
    for idx, item in enumerate(iter_dataset(json_path), start=1):
        print("=" * 80)
        print(f"Example {idx}")

        try:
            nl_query = item.get("nl_query", "<missing nl_query>")
            soql_params = item.get("soql_params", {})

            print("NL query:")
            print("  ", nl_query)

            print("SoQL params:")
            if isinstance(soql_params, dict):
                for k, v in soql_params.items():
                    print(f"  {k}: {v}")
            else:
                print("  WARNING: soql_params is not a dict:", soql_params)
                # try to skip bad ones
                continue
            
            schema_ctx = item.get("schema", "")
            if schema_ctx:
                print("Schema context:")
                print(schema_ctx)

            iucr_ctx = item.get("iucr_context", "")
            if iucr_ctx:
                print("IUCR context:")
                print(iucr_ctx)

            print("\nRunning query...")
            df = run_query(soql_params)
            if df is None:
                print("Query failed or returned no data.\n")
            else:
                print(df.head(), "\n")

        except Exception as e:
            # Catch any unexpected error and keep going
            print(f"Error while processing example {idx}: {e}\n")
            continue


if __name__ == "__main__":
    # Take an integer argument
    batch_num = None
    if len(sys.argv) > 1:
        try:
            batch_num = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Please provide an integer for batch number.")
            sys.exit(1)
            
    json_path = "data/batch_{}.json".format(batch_num) if batch_num is not None else None
    
    if json_path:
        print(f"Running dataset from {json_path}...\n")
        run_dataset(json_path)
