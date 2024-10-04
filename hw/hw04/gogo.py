#Ian Setia, Andrew Linares
#isetia@nd.edu, alinare2@nd.edu
import yaml, argparse, os
import checktests
from checktests import process_data
from spire.doc import *
from spire.doc.common import *
import concurrent.futures


def read_yaml(yaml_file):
    try:
        if not os.path.isfile(yaml_file):
            print(f"Error: the file {yaml_file} doesn't exist.")
            return None
        with open(yaml_file, 'r') as f:
            tasks = yaml.safe_load(f)
        if "tasks" not in tasks or not isinstance(tasks.get("tasks"), list):
            print("Error: the overall structure of this file is incorrect.")
            return None
        tasks_list = tasks.get("tasks")
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

def pipeline(task_dict):
    try:
        counter = 0
        for task_id in task_dict:
            task = task_dict.get(task_id)
            if process_data(task["Year"], task["Month"], task["StartText"], task["URL"], False, task["Prepend"]) == 0:
                convert(f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.docx", f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.pdf")
                convert(f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.docx", f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.pdf")
                os.remove(f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.docx")
                os.remove(f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.docx")
                
            #print(f"{task['Prepend']}{task['Year']}-{task['Month']}-WiFi.docx was successfully converted to {task['Prepend']}{task['Year']}-{task['Month']}-WiFi.pdf")
            #print(f"{task['Prepend']}{task['Year']}-{task['Month']}-Wired.docx was successfully converted to {task['Prepend']}{task['Year']}-{task['Month']}-Wired.pdf")
                #print(f"Task {task_id} Done!")
    except Exception as e:
        print(f"Exception: {e}")
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", type=str, help="name of YAML file")
    parser.add_argument("--multi", type=int, help="number of allow processors to run program (1-4)")
    args = parser.parse_args()

    data_dict = read_yaml(args.yaml_file)

    if data_dict is None:
        print(f"The YAML file \'{yaml_file}\' is empty")
        return -1

    if args.multi:
        if args.multi < 5 and args.multi > 0:
            with concurrent.futures.ProcessPoolExecutor(max_workers=args.multi) as executor:
                executor.map(pipeline, data_dict)
            print(f"Completed {len(data_dict)} task(s)!")
        else:
            proceed = input(f"{args.multi} processors are unavailable. Would you like to continue with the default option (nonparallel)? [y/n]: ")
            if proceed == 'y':
                for task_dict in data_dict:
                    pipeline(task_dict)
            else:
                print("Now exiting ...")
    else:
        for task_dict in data_dict:
            pipeline(task_dict)
        print(f"Completed {len(data_dict)} task(s)!")

if __name__ == "__main__":
    main()
