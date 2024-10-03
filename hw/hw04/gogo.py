#Ian Setia, Andrew Linares
#isetia@nd.edu, alinare2@nd.edu
import yaml, argparse, os
from checktests import process_data
from spire.doc import *
from spire.doc.common import *


def read_yaml(yaml_file):
    try:
        if not os.path.isfile(yaml_file):
            print(f"Error: the file {yaml_file} doesn't exist.")
            return None
        with open(yaml_file, 'r') as f:
            tasks = yaml.safe_load(f)
            print(tasks)
        if "tasks" not in tasks or not isinstance(tasks.get("tasks"), list):
            print("Error: the overall structure of this file is incorrect.")
            return None
        tasks_list = tasks.get("tasks")
        print(tasks_list)
        for task_dict in tasks_list:
            if not isinstance(task_dict, dict):
                print(f"The contents of the list of tasks are not dicts")
                return None
            if len(task_dict) != 1:
                print(f"There are too many elements in {tack_dict}.")
                return None
            for task_id in task_dict:
                task = task_dict.get(task_id)
                if task is None:
                    print(f"Error: {task_id} is empty")
                    return None
                if "URL" not in task or not isinstance(task["URL"], str):
                    print(f"Error: {task_id} is missing a valid URL.")
                    return None
                if "Month" not in task or not isinstance(task["Month"], int) or not (1 <= task["Month"] <= 12):
                    print(f"Error: {task_id} is missing a valid Month.")
                    return None
                if "Year" not in task or not isinstance(task["Year"], int):
                    print(f"Error: {task_id} is missing a valid Year.")
                    return None
                if "StartText" not in task or not isinstance(task["StartText"], str):
                    print(f"Error: {task_id} is missing a valid Start Text.")
                    return None
                if "Prepend" not in task or not isinstance(task["Prepend"], str):
                    print(f"Error: {task_id} is missing a valid Prepend.")
                    return None
        return tasks_list
         
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file ({yaml_file}): {e}");
        return None 

def convert(input_file, output_file):
    document = Document()
    document.LoadFromFile(input_file)
    document.SaveToFile(output_file, FileFormat.PDF)
    document.Close()

def pipeline(task_dicts):
    counter = 0
    for task_dict in task_dicts:
        for task_id in task_dict:
            task = task_dict.get(task_id)
            if process_data(task["Year"], task["Month"], task["StartText"], task["URL"], False, task["Prepend"]) == 0:
                convert(f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.docx", f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.pdf")
                convert(f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.docx", f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.pdf")
                print(f"Task {task_id} Done!")
                counter += 1
        
    print(f"Completed {counter} task(s)!")

def main():
    download_pandoc()
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=str, help="name of YAML file")
    parser.add_argument("--multi", type=int, help="number of allow processors to run program (1-4)")
    args = parser.parse_args()
    
    if args.multi:
        #write code to implement concurrent.futures package (ProcessPoolExecutor)
        pass


    data_dict = read_yaml(args.yaml_file)
    if data_dict is None:
        return -1
    pipeline(data_dict)
    print("Success")

if __name__ == "__main__":
    main()
