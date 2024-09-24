#Ian Setia
#isetia@nd.edu

import argparse, requests, json, statistics, numpy, calendar, os
from createreport import read_text_file, generate_report 
from plotdata import average_daily_performance, plot_data 

def fetch_json(url):
    try:
        response = requests.get(url)
        data = response.json()
        if not data:
            print("No data available at the URL: {}".format(url))
            return None
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data from {}: {}".format(url, e))
        return None
    except ValueError:
        print("The data at {} is not valid JSON format".format(url))
        return None
    

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
    parser.add_argument("year", type=int, help="Year to fetch data")
    parser.add_argument("month", type=int, help="Month to fetch data")
    parser.add_argument("text_file", type=str, help="Text file to insert into report")
    parser.add_argument("url", type=str, help="URL to fetch the JSON file from.")
    parser.add_argument("--all", action="store_true", help="Ignore month and year arguments and create 2 unified Word files acorss all present year and month combinations in the dataset.")

    args = parser.parse_args()
    
    if not args.url:
        print("No URL Detected. Now exiting ...")
        return


    json_data = fetch_json(args.url)

    if not json_data:
        print("Failed to retrieve or parse JSON file. Now exiting ...")
        return

    if not args.all:
        filtered_wired = filter_json(json_data, args.month, args.year, "eth0")
        filtered_wireless = filter_json(json_data, args.month, args.year, "wlan0")

        analyzed_wired = analyze_json(filtered_wired, "eth0")
        analyzed_wireless = analyze_json(filtered_wireless, "wlan0")

        text = read_text_file(args.text_file)
    
        _, days = calendar.monthrange(args.year, args.month)
        stats_wired = average_daily_performance(filtered_wired, days)
        stats_wireless = average_daily_performance(filtered_wireless, days)
        plot_data(stats_wired, "graph_wired.png") 
        plot_data(stats_wireless, "graph_wireless.png")
        output_wired = f"{args.year}-{args.month}-Wired.docx"
        output_wireless = f"{args.year}-{args.month}-WiFi.docx"
        if os.path.exists(output_wired):
            user_input = input("File {} already exists on your machine, do you want to replace it? [y/n]: ".format(output_wired)).strip().lower()
            if user_input == 'y':
                generate_report(text, analyzed_wired, "graph_wired.png", output_wired) 
            else:
                print("File {} will not be replaced.".format(output_wired))
        else:
            generate_report(text, analyzed_wired, "graph_wired.png", output_wired)
        if os.path.exists(output_wireless):
            user_input = input("File {} already exists on your machine, do you want to replace it? [y/n]: ".format(output_wireless)).strip().lower()
            if user_input == 'y':
                generate_report(text, analyzed_wireless, "graph_wireless.png", output_wireless)
            else:
                print("File {} will not be replaced.".format(output_wireless))
        else:
            generate_report(text, analyzed_wireless, "graph_wireless.png", output_wireless) 
        os.remove("graph_wired.png")
        os.remove("graph_wireless.png")
    else:
        print("TO BE IMPLEMENTED")

if __name__ == "__main__":
    main()
