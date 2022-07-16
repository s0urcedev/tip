# imports ------------------------------------------------------
import os
import sys
import json
import getpass
import datetime
# --------------------------------------------------------------

# getting path -------------------------------------------------
if getattr(sys, 'frozen', False):
    APP_PATH: str = os.path.dirname(sys.executable)
elif __file__:
    APP_PATH: str = os.path.dirname(__file__)
APP_PATH = APP_PATH.replace("\\", "/")
# --------------------------------------------------------------

USER = getpass.getuser() # getting USER

def get_date() -> str: # functions for getting date
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_spent_time(start: str, end: str) -> int: # functions for spent time
    date_end: datetime.datetime = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    date_start: datetime.datetime = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    delta: dict = {}
    delta['days']: int = (date_end.year - date_start.year) * 365 + (date_end.month - date_start.month) * 30 + (date_end.day - date_start.day)
    delta['hours']: int = date_end.hour - date_start.hour
    delta['minutes']: int = date_end.minute - date_start.minute
    if delta['minutes'] < 0:
        delta['hours'] -= 1
        if delta['hours'] < 0:
            delta['days'] -= 1
            delta['hours'] += 24
        delta['minutes'] += 60
    delta['seconds']: int = date_end.second - date_start.second
    if delta['seconds'] < 0:
        delta['minutes'] -= 1
        if delta['minutes'] < 0:
            delta['hours'] -= 1
            if delta['hours'] < 0:
                delta['days'] -= 1
                delta['hours'] += 24
            delta['minutes'] += 60
        delta['seconds'] += 60
    return f"{delta['days']} days, {delta['hours']} hours {delta['minutes']} minutes {delta['seconds']} seconds"

def list_tasks() -> None: # function for printing list of tasks
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
            open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
            opened.append(f"OPENED: {key} [{open_date}]")
            if len(f"OPENED: {key} [{open_date}]") > max_len:
                max_len = len(f"OPENED: {key} [{open_date}]")
        elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
            open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
            close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
            closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
            if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("You don't have tasks")

def open_task(name: str) -> None: # function for opening task
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    tip_lock[USER]["tasks"][name] = {
        "open_date": get_date(),
        "close_date": "—",
        "state": "OPENED"
    }
    with open(f"{APP_PATH}/tip-lock.json", 'w') as tl:
        tl.write(json.dumps(tip_lock, ensure_ascii=False, indent=4))
        
def close_task(name: str) -> None: # function for closing task
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    tip_lock[USER]["tasks"][name] = {
        "open_date": tip_lock[USER]["tasks"][name]["open_date"],
        "close_date": get_date(),
        "state": "CLOSED"
    }
    with open(f"{APP_PATH}/tip-lock.json", 'w') as tl:
        tl.write(json.dumps(tip_lock, ensure_ascii=False, indent=4))
    time_spent: int = get_spent_time(tip_lock[USER]["tasks"][name]["open_date"], tip_lock[USER]["tasks"][name]["close_date"])
    print(f"You spent on this task: {time_spent}")

def delete_task(name: str) -> None: # function for deleting task
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    tip_lock[USER]["tasks"].pop(name, {})
    with open(f"{APP_PATH}/tip-lock.json", 'w') as tl:
        tl.write(json.dumps(tip_lock, ensure_ascii=False, indent=4))
    
def search_year(year: str) -> None: # function for searching by year
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").year == int(year):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

def search_month(month: str) -> None: # function for searching by month
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").month == int(month):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

def search_day(day: str) -> None: # function for searching by day
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").day == int(day):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

def search_hour(hour: str) -> None: # function for searching by hour
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").hour == int(hour):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

def search_minute(minute: str) -> None: # function for searching by minute
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").minute == int(minute):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

def search_second(second: str) -> None: # function for searching by second
    with open(f"{APP_PATH}/tip-lock.json", 'r') as tl:
        tip_lock: dict = json.loads(tl.read())
    opened: list[str] = []
    closed: list[str] = []
    max_len: int = 0
    for key in tip_lock[USER]["tasks"]:
        if datetime.datetime.strptime(tip_lock[USER]["tasks"][key]["open_date"], "%Y-%m-%d %H:%M:%S").second == int(second):
            if tip_lock[USER]["tasks"][key]["state"] == "OPENED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                opened.append(f"OPENED: {key} [{open_date}]")
                if len(f"OPENED: {key} [{open_date}]") > max_len:
                    max_len = len(f"OPENED: {key} [{open_date}]")
            elif tip_lock[USER]["tasks"][key]["state"] == "CLOSED":
                open_date: str = tip_lock[USER]["tasks"][key]["open_date"]
                close_date: str = tip_lock[USER]["tasks"][key]["close_date"]
                closed.append(f"CLOSED: {key} [{open_date} — {close_date}]")
                if len(f"CLOSED: {key} [{open_date} — {close_date}]") > max_len:
                    max_len = len(f"CLOSED: {key} [{open_date} — {close_date}]")
    if max_len > 0:
        print('\n'.join(closed))
        print('-' * max_len)
        print('\n'.join(opened))
    else:
        print("Task with this filter not found")

if __name__ == "__main__":
    if len(sys.argv) == 1: # 'tip'
        print("Hello, I'm tip")
        print("\nWhat I can do:\ninit — init list for user\nlist — show all tasks\nopen — open task\nclose — close task\nsearch — search tasks")
    elif sys.argv[1] == "init": # 'tip init'
        with open(f"{APP_PATH}/tip-lock.json", 'w') as tl:
            tl.write(json.dumps({USER: {"tasks": {}}}, ensure_ascii=False, indent=4))
    elif sys.argv[1] == "list": # 'tip list'
        list_tasks()
    elif sys.argv[1] == "open" and len(sys.argv) > 2: # 'tip open'
        for i in range(2, len(sys.argv)):
            open_task(sys.argv[i])
    elif sys.argv[1] == "close" and len(sys.argv) > 2: # 'tip close'
        for i in range(2, len(sys.argv)):
            close_task(sys.argv[i])
    elif sys.argv[1] == "delete" and len(sys.argv) > 2: # 'tip delete'
        for i in range(2, len(sys.argv)):
            delete_task(sys.argv[i])
    elif sys.argv[1] == "search" and len(sys.argv) == 4: # 'tip search'
        if sys.argv[2] == "year": # 'tip search year'
            search_year(sys.argv[3])
        elif sys.argv[2] == "month": # 'tip search month'
            search_month(sys.argv[3])
        elif sys.argv[2] == "day": # 'tip search day'
            search_day(sys.argv[3])
        elif sys.argv[2] == "hour": # 'tip search hour'
            search_hour(sys.argv[3])
        elif sys.argv[2] == "minute": # 'tip search minute'
            search_minute(sys.argv[3])
        elif sys.argv[2] == "second": # 'tip search second'
            search_second(sys.argv[3])
    else:
        print("Uncorrect arguments")