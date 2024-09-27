#Ian Setia
#isetia@nd.edu

import argparse, json
import matplotlib.pyplot as plt
import numpy as np 

def average_daily_performance(data, days):
    # Creates a dictionary that holds the total sum, total count, and average tput for each day in the month
    # (or in the case of the --all, the same data for each month in the year)
    daily_average = {day : {"total" : 0, "count" : 0, "average" : 0} for day in range(1, days+1)}
    
    # Fills dictionary with data
    for entry in data:
        day = int(entry["timestamp"][8:10]) if days != 12 else int(entry["timestamp"][5:7])
        if day in daily_average:
            daily_average[day]["total"] = daily_average[day]["total"] + entry["tput_mbps"]
            daily_average[day]["count"] += 1
    # Calculates average for each bar in the graph
    for day, stat in daily_average.items():
        stat["average"] = (stat["total"]/stat["count"]) if stat["count"] != 0 else 0
    return daily_average
         
def plot_data(data_dict, out_file):
    days = list(data_dict.keys())
    averages = [stat["average"] for stat in data_dict.values()]

    fig, ax = plt.subplots()
    ax.grid()
    ax.bar(days, averages)
    plt.xlabel("Day" if 27 in days else "Month")
    plt.ylabel("Average Throughput (Mb/s)")
    plt.title("Daily Average Throughput" if 27 in days else "Monthly Average Throughput")
    plt.savefig(out_file)
    plt.close()

    

def main():
    parser = argparse.ArgumentParser(description="Read JSON and outputs file")

    parser.add_argument("json", type=str, help="json to read")
    parser.add_argument("days", type=int, help="number of days in the month")
    parser.add_argument("output", type=str, help="name of output file")

    args = parser.parse_args()

    theData = json.loads(open(args.json).read())
    avg = average_daily_performance(theData, args.days)

    print(avg)
    plot_data(avg, args.output)

    
    

if __name__ == "__main__":
    main()
