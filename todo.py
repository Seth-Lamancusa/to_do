import sys
import json
from datetime import date, timedelta
from validation import *
from user_input import *
from helpers import *
from managers import *


# Display


def display_items(items):
    """
    Displays the items in a readable format.

    Parameters:
        items (list): A list of item dictionaries.

    Raises:
        ValueError: if items is not valid
    """

    if not is_valid_items(items):
        raise ValueError("Items is not valid")

    if not items:
        print(
            """
        No items in the list.
        """
        )
        return

    print("============ Items ============")
    for i, item in enumerate(items, start=1):
        print(
            f"{i}. {item['description']} ({item['type']}) ({'active' if item['active'] else 'inactive'})"
        )

        if item["type"] == "goal":
            print(f"   Start Date: {item['start_date']}")
            print(f"   Deadline: {item['deadline']}")
            print(f"   Schedule: {item['gschedule']}")
        elif item["type"] == "routine":
            print(f"   Frequency: {item['frequency']}")
            print(f"   Schedule: {item['rschedule']}")

        print()


def display_items_for_date(data, date_):
    """
    Parameters:
        data (dict): The data to display.
        date (datetime.date): The date to display.

    Raises:
        ValueError: if data is not valid
        ValueError: if date is not valid
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_date(date_):
        raise ValueError("Date is not valid")

    items = get_items_for_date(data, date_)
    year = int(date_.isoformat().split("-")[0])
    month = int(date_.isoformat().split("-")[1])
    day = int(date_.isoformat().split("-")[2])
    weekday = date(year, month, day).weekday()
    print(f"=== {weekday}, {date_.isoformat()} ===")
    display_items(items)


def enter_day_view(data):
    """
    Parameters:
        data (dict): The data to enter day view with.

    Raises:
        ValueError: if data is not valid
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")

    date_ = date.today()
    while True:
        display_items_for_date(data, date_)
        choice = input(
            "Enter b for previous day, n for next day, or r to return to menu: "
        )
        if choice == "b":
            date_ -= timedelta(days=1)
        elif choice == "n":
            date_ += timedelta(days=1)
        elif choice == "r":
            return
        else:
            print("Invalid input")


def display_controls():
    print(
        """
    =============== Controls ===============
    ? - display controls
    a - add item
    d - delete item
    ed - edit item attribute
    di - display all items
    e - enter day view
    q - quit

    """
    )


# Control flow


def save_data(data):
    def date_converter(obj):
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    try:
        with open(DATAFILE, "w", encoding="utf-8") as f:
            json.dump(data, f, default=date_converter)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
        print(f"Error: {str(e)} occurred while saving data to file {DATAFILE}.")


def process_value(value):
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return value  # not a date
    elif isinstance(value, list):
        return [process_value(item) for item in value]
    return value


def iso_to_date(dct):
    for key, value in dct.items():
        dct[key] = process_value(value)
    return dct


def retrieve_data():
    try:
        with open(DATAFILE, "r", encoding="utf-8") as f:
            return json.load(f, object_hook=iso_to_date)
    except FileNotFoundError:
        print("Error: no data file")


def quit_program(data):
    save_data(data)
    print("Goodbye!")
    sys.exit()


# Main


DATAFILE = "data.json"
data = retrieve_data()


def main():
    while True:
        choice = input("Enter choice or '?' for controls: ")
        if choice == "?":
            display_controls()
        elif choice == "a":
            new_item = prompt_for_new_item(data)
            if not new_item is None:
                add_item(data, new_item)
                print("Item added successfully.")
            else:
                print("Item not added.")
        elif choice == "di":
            display_items(data["items"])
        elif choice == "e":
            enter_day_view(data)
        elif choice == "d":
            item_desc = prompt_for_existing_item_desc(data)
            if not item_desc is None:
                delete_item(data, item_desc)
                print("Item deleted successfully.")
            else:
                print("Item not deleted.")
        elif choice == "q":
            quit_program(data)
        elif choice == "ed":
            prompt_for_edit_item(data)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
