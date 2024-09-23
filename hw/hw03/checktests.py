#Ian Setia
#isetia@nd.edu

import argparse, requests, json, statistics, numpy

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

def analyze_json(data, interface):
    interface_data = [d for d in data if d.get("interface") == interface]
    tput = [i["tput_mbps"] for i in interface_data]
    unique_periods = set()
    period = ""
    for i in interface_data:
        unique_periods.add(i["timestamp"][:7])
        period = i["timestamp"][:7]
    tput = sorted(tput)
    data_dict = {
        "Period" : period if len(unique_periods) == 1 else "All",
        "Interface" : "Wired" if interface == "eth0" else "Wireless",
        "Num Points" : len(tput),
        "Min" : min(tput),
        "Max" : max(tput),
        "Mean" : statistics.mean(tput),
        "Median" : statistics.median(tput),
        "Std Dev" : statistics.stdev(tput) if len(tput) > 1 else 0,
        "10th Percentile" : numpy.percentile(tput, 10),
        "90th Percentile" : numpy.percentile(tput, 90) 
    }
    return data_dict

def print_dict(dictionary):
    for key, value in dictionary.items():
        print("{}: {}".format(key, value))
    

def main():
    parser = argparse.ArgumentParser(description="Fetch JSON file from given URL.")
    parser.add_argument("url", type=str, help="URL to fetch the JSON file from.")

    args = parser.parse_args()

    json_data = fetch_json(args.url)
    
    #if json_data is not None:
    #   print(json.dumps(json_data, indent=4))

    filtered = filter_json(json_data)
    #print(json.dumps(filtered, indent=4))

    analyzed = analyze_json(filtered, "eth0")
    print_dict(analyzed)

    filtered = filter_json(json_data, interface="wlan0")

    analyzed = analyze_json(filtered, "wlan0")
    print_dict(analyzed)

if __name__ == "__main__":
    main()
