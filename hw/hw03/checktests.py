#Ian Setia
#isetia@nd.edu

import argparse, requests, json

def fetch_json(url):
    response = requests.get(url)
    data = response.json()
    return data
    
def filter_json(data, month=5, year=2024, interface="eth0"):
    filtered_data = []
    for entry in data:
        time_year = int(entry.get("timestamp")[:4])
        time_month = int(entry.get("timestamp")[5:7])
        if time_year == year and time_month == month and entry.get("interface") == interface:
            filtered_data.append(entry)
    return filtered_data

def main():
    parser = argparse.ArgumentParser(description="Fetch JSON file from given URL.")
    parser.add_argument("url", type=str, help="URL to fetch the JSON file from.")

    args = parser.parse_args()

    json_data = fetch_json(args.url)
    
    if json_data is not None:
        print(json.dumps(json_data, indent=4))

    filtered = filter_json(json_data)
    print(json.dumps(filtered, indent=4))

if __name__ == "__main__":
    main()
