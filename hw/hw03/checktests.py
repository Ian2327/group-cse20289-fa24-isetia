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
    
# Filters a json stored in data variable by the month and year and interface given (default is 5 and 2024 and eth0) 
def filter_json(data, month=5, year=2024, interface="eth0"):
    filtered_data = []
    # If month and year are set to None, then the --all flag has been triggered and will skip filtering by month and year
    if(month is None and year is None):
        for entry in data:
            if entry.get("interface") == interface and entry.get("direction") == "downlink" and entry.get("type") == "iperf":
                filtered_data.append(entry)
    else:
        for entry in data:
            # filters the year
            time_year = int(entry.get("timestamp")[:4])
            # filters the month
            time_month = int(entry.get("timestamp")[5:7])
            if time_year == year and time_month == month and entry.get("interface") == interface and entry.get("direection") == "downlink" and entry.get("type") == "iperf":
                filtered_data.append(entry)
    return filtered_data

def analyze_json(data, interface):
    interface_data = [d for d in data if d.get("interface") == interface] # only includes correct interfaced data in list to analyze
    tput = [i["tput_mbps"] for i in interface_data]
    unique_periods = set() # used to determine if data is all from a single year and month or not
    period = ""
    for i in interface_data:
        unique_periods.add(i["timestamp"][:7])
        period = i["timestamp"][:7]
    tput = sorted(tput)
    # stats have default values in case json is lacking data
    data_dict = {
        "Period" : period if len(unique_periods) == 1 else "All",
        "Interface" : "Wired" if interface == "eth0" else "Wireless",
        "Num Points" : len(tput),
        "Min" : min(tput) if tput else 0,
        "Max" : max(tput) if tput else 0,
        "Mean" : statistics.mean(tput) if tput else 0,
        "Median" : statistics.median(tput) if tput else 0,
        "Std Dev" : statistics.stdev(tput) if len(tput) > 1 else 0,
        "10th Percentile" : numpy.percentile(tput, 10) if tput else 0,
        "90th Percentile" : numpy.percentile(tput, 90) if tput else 0
    }
    return data_dict

# Custom function for the --all flag to generate its report due to differing function inputs
def generate_all_report(data, text, interface, output):
    filtered = filter_json(data, None, None, interface)
    analyzed = analyze_json(filtered, interface)
    stats = average_daily_performance(filtered, 12)
    plot_data(stats, "all.png")
    if os.path.exists(output):
        user_input = input("File {} already exists on your machine, do you want to replace it? [y/n]: ".format(output)).strip().lower()
        if user_input == 'y':
            generate_report(text, analyzed, "all.png", output) 
        else:
           print("File {} will not be replaced.".format(output))
    else:
        generate_report(text, analyzed, "all.png", output)
    os.remove("all.png")
    

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

    if not os.path.exists(args.text_file):
        print("The text file {} does not exist. Now exiting ...".format(args.text_file))
        return
    
    text = read_text_file(args.text_file)

    # Checks for --all flag
    if not args.all:
        filtered_wired = filter_json(json_data, args.month, args.year, "eth0")
        filtered_wireless = filter_json(json_data, args.month, args.year, "wlan0")

        analyzed_wired = analyze_json(filtered_wired, "eth0")
        analyzed_wireless = analyze_json(filtered_wireless, "wlan0")

        #text = read_text_file(args.text_file)
    
        _, days = calendar.monthrange(args.year, args.month)
        stats_wired = average_daily_performance(filtered_wired, days)
        stats_wireless = average_daily_performance(filtered_wireless, days)
        plot_data(stats_wired, "graph_wired.png") 
        plot_data(stats_wireless, "graph_wireless.png")
        output_wired = f"{args.year}-{args.month}-Wired.docx"
        output_wireless = f"{args.year}-{args.month}-WiFi.docx"

        # Check for duplicate Wired docx output file
        if os.path.exists(output_wired):
            user_input = input("File {} already exists on your machine, do you want to replace it? [y/n]: ".format(output_wired)).strip().lower()
            if user_input == 'y':
                generate_report(text, analyzed_wired, "graph_wired.png", output_wired) 
            else:
                print("File {} will not be replaced.".format(output_wired))
        else:
            generate_report(text, analyzed_wired, "graph_wired.png", output_wired)

        # Checks for duplicate WiFi docx output file
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
        filtered_wired_all = filter_json(json_data, None, None, "eth0")
        filtered_wireless_all = filter_json(json_data, None, None, "wlan0")

        generate_all_report(filtered_wired_all, text, "eth0", "All-Wired.docx")
        generate_all_report(filtered_wireless_all, text, "wlan0", "All-WiFi.docx")

if __name__ == "__main__":
    main()
