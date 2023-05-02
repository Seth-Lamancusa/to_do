import sys
import json
from validation import *
from user_input import *
from helpers import *
from datetime import date, timedelta


DATAFILE = 'data.json'


# Edit


def add_item(data, item):
    """
    Parameters:
        data (dict): data to add to
        item (dict): item to add

    Returns:
        None

    Raises:
        ValueError: if item is not valid
        ValueError: if data is not valid data
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_item(item):
        raise ValueError("Item is not valid")

    data["items"].append(item)


def delete_item(data, item_desc):
    """
    Parameters:
        data (dict): The data to delete an item from.
        item_desc (int): The id of the item to delete.

    Returns:
        dict: The data after deleting the item.

    Raises:
        ValueError: if data is not valid
        ValueError: if item_desc is not valid
        ValueError: if item_desc is not in data
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_description(item_desc):
        raise ValueError("item_desc is not valid")
    if item_desc not in [item["description"] for item in data["items"]]:
        raise ValueError("item_desc is not in data")

    for item in data["items"]:
        if item["description"] == item_desc:
            data["items"].remove(item)
            return data


def toggle_item_active(data, item_desc):
    """
    Parameters:
        data (dict): The data to toggle the active status of an item in.
        item_desc (str): The id of the item to toggle the active status of.

    Returns:
        dict: The data after toggling the active status of the item.

    Raises:
        ValueError: if data is not valid
        ValueError: if item_desc is not valid
        ValueError: if item_desc is not in data
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_description(item_desc):
        raise ValueError("item_desc is not valid")
    if item_desc not in [item["description"] for item in data["items"]]:
        raise ValueError("item_desc is not in data")

    for item in data["items"]:
        if item["description"] == item_desc:
            item["active"] = not item["active"]
            return data


def edit_item_attribute(data, item_desc, attribute, new_value):
    """
    Parameters:
        data (dict): The data to edit an item in.
        item_desc (str): The id of the item to edit.
        attribute (str): The attribute to edit.
        new_value (str): The new value for the attribute.

    Returns:
        dict: The data after editing the item.

    Raises:
        ValueError: if data is not valid
        ValueError: if item_desc is not valid
        ValueError: if attribute is not valid
        ValueError: if new_value is not valid
        ValueError: if item_desc is not in data
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_description(item_desc):
        raise ValueError("item_desc is not valid")
    if not is_valid_attribute_key(attribute):
        raise ValueError("attribute is not valid")
    if not is_valid_attribute_value(attribute, new_value, get_item(item_desc, data)):
        raise ValueError("new_value is not valid")
    if item_desc not in [item["description"] for item in data["items"]]:
        raise ValueError("item_desc is not in data")

    for item in data["items"]:
        if item["description"] == item_desc:
            item[attribute] = new_value


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
        print('''
        No items in the list.
        ''')
        return

    print("============ Items ============")
    for i, item in enumerate(items, start=1):
        print(
            f"{i}. {item['description']} ({item['type']}) ({'active' if item['active'] else 'inactive'})")

        if item['type'] == "goal":
            print(f"   Start Date: {item['start_date']}")
            print(f"   Deadline: {item['deadline']}")
            print(f"   Schedule: {item['gschedule']}")
        elif item['type'] == "routine":
            print(f"   Frequency: {item['frequency']}")
            print(f"   Schedule: {item['rschedule']}")

        print()


def display_items_for_date(data, date_str):
    """
    Parameters:
        data (dict): The data to display.
        date (str): The date to display.

    Raises:
        ValueError: if data is not valid
        ValueError: if date is not valid
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_iso_date(date_str):
        raise ValueError("Date is not valid")

    items = get_items_for_date(data, date_str)
    year = int(date_str.split("-")[0])
    month = int(date_str.split("-")[1])
    day = int(date_str.split("-")[2])
    weekday = date(year, month, day).weekday()
    print(f"=== {weekday}, {date_str} ===")
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
        display_items_for_date(data, date_.isoformat())
        choice = input(
            "Enter b for previous day, n for next day, or r to return to menu: ")
        if choice == "b":
            date_ -= timedelta(days=1)
        elif choice == "n":
            date_ += timedelta(days=1)
        elif choice == "r":
            return
        else:
            print("Invalid input")


def display_controls():
    print('''
    =============== Controls ===============
    ? - display controls
    a - add item
    di - display all items
    s - display items for a specific date
    e - enter day view
    d - delete item
    t - toggle item active status
    q - quit

    ''')


# Control flow


def save_data(data):
    try:
        with open(DATAFILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
        print(
            f"Error: {str(e)} occurred while saving data to file {DATAFILE}.")


def retrieve_data():
    try:
        with open(DATAFILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print('Error: no data file')


def quit_program(data):
    save_data(data)
    print('Goodbye!')
    sys.exit()


# Main


def main():
    data = retrieve_data()

    while True:
        choice = input("Enter choice or '?' for controls: ")
        if choice == '?':
            display_controls()
        elif choice == 'a':
            add_item(data, prompt_for_new_item())
            print("Item added successfully.")
        elif choice == 'di':
            display_items(data['items'])
        elif choice == 's':
            display_items_for_date(data, prompt_for_valid_date())
        elif choice == 'e':
            enter_day_view(data)
        elif choice == 'd':
            delete_item(data, prompt_for_existing_item_desc(data))
            print("Item deleted successfully.")
        elif choice == 't':
            toggle_item_active(data, prompt_for_existing_item_desc(data))
            print("Item active status toggled successfully.")
        elif choice == 'q':
            quit_program(data)
        elif choice == 'ed':
            item_desc = prompt_for_existing_item_desc(data)
            item = get_item(item_desc, data)
            attribute = prompt_for_existing_attribute(item)
            new = prompt_for_valid_attribute_value(attribute, item)
            edit_item_attribute(data, item_desc, attribute, new)
            print("Item edited successfully.")
        else:
            print('Invalid choice')


main()
