from validation import *
from datetime import date, datetime
from models import UserData


# Helpers


def get_item(item_desc, data):
    """
    Gets an item from the data with the given description, or None.

    Parameters:
        item_desc (str): The description of the item to get.
        data (list): The data to get the item from.

    Returns:
        dict: The item with the given description, None if not found.
    """

    for item in data["items"]:
        if item["description"] == item_desc:
            return item

    return None


def get_compatibility_dict(item):
    """
    Gets a compatibility dictionary for the given item.

    Parameters:
        item (dict): The item to get a compatibility dictionary for.

    Returns:
        dict: A compatibility dictionary for the given item.
    """

    if item["type"] == "goal":
        return {
            "gschedule": item["gschedule"],
            "start_date": item["start_date"],
            "deadline": item["deadline"],
        }
    elif item["type"] == "routine":
        return {"rschedule": item["rschedule"], "frequency": item["frequency"]}


def get_items_for_date(data, date_):
    """
    Parameters:
        data (UserData): The data to get items from.
        date_ (datetime.date): The date to get items for.

    Returns:
        list: A list of item dictionaries.

    Raises:
        ValueError: if data is not valid
        ValueError: if date is not valid
    """

    if not type(data) == UserData:
        raise ValueError("Data is not valid")
    if not type(date_) == date:
        raise ValueError("Date is not valid")

    items = []

    for item in data.items:
        if item.type == "goal":
            if date_in_gschedule(item.gschedule, date_):
                items.append(item)
        elif item.type == "routine":
            if date_in_rschedule(item.frequency, item.rschedule, date_):
                items.append(item)

    return items


def date_in_gschedule(gschedule, date_):
    """
    Parameters:
        gschedule (list): A list of lists containing a date and time.
        date (datetime.date): The date to check.

    Returns:
        bool: True if the date is in the gschedule, False otherwise.

    Raises:
        ValueError: if date is not valid
    """

    if not is_valid_date(date_):
        raise ValueError("Date is not valid")

    for item in gschedule:
        if item[0] == date_:
            return True

    return False


def date_in_rschedule(frequency, rschedule, date_):
    """
    Parameters:
        frequency (str): The frequency of the rschedule.
        rschedule (list): A list of lists containing a time.
        date (datetime.date): The date to check.

    Returns:
        bool: True if the date is in the rschedule, False otherwise.

    Raises:
        ValueError: if frequency is not valid
        ValueError: if rschedule is not valid
        ValueError: if date is not valid
    """

    if not is_valid_frequency(frequency):
        raise ValueError("frequency is not valid")
    if not is_valid_rschedule(rschedule):
        raise ValueError("rschedule is not valid")
    if not is_valid_date(date_):
        raise ValueError("Date is not valid")

    if frequency == "day":
        return True

    if frequency == "week":
        day = date_.weekday()
        for item in rschedule:
            if item[0] == day:
                return True

    if frequency == "month":
        day = date_.day
        for item in rschedule:
            if item[0] == day:
                return True

    if frequency == "year":
        day = date_.timetuple().tm_yday
        for item in rschedule:
            if item[0] == day:
                return True

    return False


def item_in_data(data, item_desc):
    """
    Parameters:
        data (dict): The data to check for the description in.
        item_desc (int): The id of the item to check for.

    Returns:
        bool: True if the description exists, False otherwise.

    Raises:
        ValueError: if data is not valid
        ValueError: if item_desc is not valid
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_valid_description(item_desc):
        raise ValueError("item_desc is not valid")

    for item in data["items"]:
        if item["description"] == item_desc:
            return True

    return False
