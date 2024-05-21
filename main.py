import csv, sys, os
from datetime import date, datetime
import pandas as pd 
from tabulate import tabulate


file_name = "ToDoList.csv"
fieldnames = ["Task","Status","Date"]
df = None

def print_table():
    table = [["V","View Task"] ,["A","Add Task"], ["U","Update Task"], ["S", "Update Status"],
              ["D","Delete Task"],["Q","Quit"]]
    headers = ["Commands", "Actions"]
    print(tabulate(table, headers, tablefmt="rounded_outline"))


def main():
    app_running = True
    print("Welcome to the to do list app")
    print("----------------------------")

    while app_running:
        global df
        create_to_do_list_table()
        df = pd.read_csv(file_name)
        print_table()
        command = input("Enter a command: ").upper()
        if command == "V":
            view_task()
        
        elif command == "A":
            task_to_add = input("Add the task: ")
            date = input("Date: ")
            if (validate_date(date)):
                print(add_task(task_to_add, date))
                
        elif command == "U":
            index = input("Enter index to update task: ")
            if (check_index(index)):
                task = input("Enter the task: ")
                print(update_task(index, task))
     
        elif command == "D":
            index = input("Enter the index to delete: ")
            if (check_index(index)):
                print(delete_task(index))

        elif command == "S":
            index = input("Enter the index to update status: ")
            if (check_index(index)):
                print(update_status(index))
            
        
        elif command == "Q":
            sys.exit("Thank you")

        else:
            print("Invalid input")


            
def create_to_do_list_table():
     global field_names, df
     if not os.path.exists(file_name):
        with open(file_name, mode="w",newline="") as write_file:
            csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames, delimiter=",")
            csv_writer.writeheader()


def view_task():
    with open(file_name, mode="r") as file:
        csv_reader = csv.DictReader(file, delimiter=",")
        table_data= {"ID": [], "Task": [], "Status": [], "Date": []}
        index = 1
        for row in csv_reader:
            table_data["ID"].append(index)
            table_data["Task"].append(row["Task"])
            table_data["Status"].append(row["Status"])
            table_data["Date"].append(row["Date"])
            index += 1
        print(tabulate(table_data, headers="keys", tablefmt="rounded_outline"))
    

def add_task(task,date):
    global fieldnames, df
    df = df._append({"Task": task, "Status": "Unfinished","Date": date}, ignore_index = True)
    df.to_csv(file_name, index=False)
    return f"Task '{task}' has been added"



def delete_task(index):
    global df
    df = df.drop(index = int(index) - 1)
    df.to_csv(file_name, index=False)
    return f"Task {index} has been deleted."

            

def update_task(index, task):
    global fieldnames, df
    df.at[int(index) - 1, "Task"] = task
    df.to_csv(file_name, index=False)
    return f"Task {index} has been updated to {task}."


def update_status(index):
    global df
    df.at[int(index) - 1, "Status"] = "Finished"
    df.to_csv(file_name, index=False)
    return f"Task {index} is finished"
    


def check_index(index):
    global df
    try:
        index = int(index)
        if (index <= 0 or index > len(df)):
            raise IndexError
        
    except ValueError:
         print("Please enter an integer.")
         return False
    
    except IndexError:
         print(f"Task {index} doesn't exist.")
         return False
    else:
        return True  
    


def validate_date(user_date_input, format="%m/%d/%Y"):
    try:
         bool(datetime.strptime(user_date_input, format))  
    except:
        print("Invalid Date")
        return False
    else:
        year, month, day = str(date.today()).split("-")
        user_month, user_day, user_year = user_date_input.split("/")

        calendar_date = date(int(year), int(month), int(day))
        user_date = date(int(user_year), int(user_month), int(user_day))

        if user_date >= calendar_date:
            return True
        print("The date must be greater than or equal to current date")          


if __name__ == "__main__":
    main()