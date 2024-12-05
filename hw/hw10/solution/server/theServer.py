import sys, json, requests, signal, statistics, zmq
from processdata import *

def exit(signal, frame):
    print("Shutting down server")
    sys.exit(0)

def parse_commands(command):
    parts = [part.strip() for part in command.split(",")]
    if len(parts) < 4:
        return None, "failure, incomplete/invalid command"
    stat, date, time, filters = parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else None
    if not filters:
        filters = "interface=eth0;direction=downlink;type=iperf" # example uses iface, dir, and type but
                                                                 # json has interface, direction, and type
    else:
        fixed_filters = []
        try:
            filter_parts = filters.split(";")
            for filter_part in filter_parts:
                key_val = filter_part.split("=")
                if len(key_val) != 2:
                    return None, f"failure, malformed filter: {filter_part}"
                key, val = key_val
                if key in {"iface", "interface"}:
                    fixed_filters.append(f"interface={val}")
                elif key in {"dir", "direction"}:
                    fixed_filters.append(f"direction={val}")
                elif key in {"type"}:
                    fixed_filters.append(f"type={val}")
                else:
                    return None, f"failure, unknown filter key: {key}"
            filters = ";".join(fixed_filters)
        except Exception as e:
            return None, f"failure, error processing filters: {e}"

    return (stat, date, time, filters), None

def calculate_stat(stat, data):
    if stat == "count":
        return len(data)
    elif stat == "mean":
        return statistics.mean([d['tput_mbps'] for d in data])
    elif stat == "median":
        return statistics.median(d['tput_mbps'] for d in data)
    elif stat == "min":
        return min(d['tput_mbps'] for d in data)
    elif stat == "max":
        return max(d['tput_mbps'] for d in data)
    elif stat == "stddev":
        return statistics.stdev(d['tput_mbps'] for d in data)
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 theServer.py <data_url> <port>")
        sys.exit(1)

    data_url = sys.argv[1]
    port = int(sys.argv[2])
    try:
        with open(data_url, 'r') as f:
            data = json.load(f)
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            #try:
            socket.bind(f"tcp://*:{port}") 
            print(f"Server started successfully - listening on Port {port}")
            #except:
            #    print("Failed to bind on port" + str(port))
            #    sys.exit(1)
            signal.signal(signal.SIGINT, exit)

            list_queue = []

            while True:
                print("Waiting for a new command")
                command = socket.recv_string()
                print(f"RCVD: {command}")
                if command == "exit":
                    socket.send_string("success, exiting")
                    break
                if command == "more":
                    if list_queue:
                        record = list_queue.pop(0)
                        response = f"success, {len(list_queue)}, " + ", ".join(f"{k}, {v}" for k, v in record.items())
                    else:
                        response = "failure, no more data to send"
                    socket.send_string(response)
                    continue
                parsed_command, error = parse_commands(command)
                if error:
                    socket.send_string(error)
                    continue
                stat, date, time, filters = parsed_command
                if stat not in ["list", "count", "mean", "stddev", "median", "min", "max"]:
                    socket.send_string(f"failure, invalid command {stat}")
                    continue
                try:
                    filtered_records = filter_data(data, date, time, filters)
                except Exception as e:
                    socket.send_string(f"failure, error filtering data: {e}")
                    continue
                if stat == "list":
                    if isinstance(filtered_records, list):
                        list_queue.extend(filtered_records)  # Add individual records to the queue
                    else:
                        list_queue.append(filtered_records)
                    response = f"success, {len(list_queue)}"
                else:
                    try:
                        result = calculate_stat(stat, filtered_records)
                        if result is not None:
                            response = f"success, {stat}, {result:.4f}" if isinstance(result, float) else f"success, {stat}, {result}"
                        else:
                            response = "failure, bad command - " + stat
                    except Exception as e:
                        response = f"failure, error processing stat: {e}"

                socket.send_string(response)
    except Exception as e:
        print(f"Error loading data from {data_url}")
        sys.exit(1)
    
    
