import sys
import json
from datetime import date, datetime


# TODO
# Fix duplicates
# Add priorities key to data


DATAFILE = 'data.json'


def is_valid_data(data):
    """
    Parameters:
        data (dict): data to validate

    Returns:
        bool: True if data is valid, False otherwise
    """

    if not isinstance(data, dict):
        return False

    if len(data) != 1:
        return False
    if "items" not in data:
        return False

    descriptions = [item["description"] for item in data["items"]]
    if len(descriptions) != len(set(descriptions)):
        return False

    return is_valid_items(data["items"])


def is_valid_items(items):
    """
    Parameters:
        items (list): items to validate

    Returns:
        bool: True if items are valid, False otherwise
    """

    if not isinstance(items, list):
        return False

    for item in items:
        if not is_valid_item(item):
            return False

    return True


def is_valid_item(item):
    """
    Parameters:
        item (dict): item to validate

    Returns:
        bool: True if item is valid, False otherwise
    """

    if not isinstance(item, dict):
        return False

    keys = {"description", "type"}
    try:
        if item.get("type") == "goal":
            keys.update({"start_date", "deadline", "gschedule"})
        elif item.get("type") == "routine":
            keys.update({"frequency", "rschedule"})
        else:
            return False
    except KeyError:
        return False

    if keys != set(item.keys()):
        return False

    if not (is_valid_description(item["description"]) and is_valid_type(item["type"])):
        return False

    if item["type"] == "goal":
        return (is_valid_dates(item["start_date"], item["deadline"]) and
                is_valid_gschedule(item["gschedule"], item["start_date"], item["deadline"]))
    elif item["type"] == "routine":
        return (is_valid_frequency(item["frequency"]) and
                is_valid_rschedule(item["rschedule"], item["frequency"]))


def is_valid_description(description):
    """
    Parameters:
        description (str): description to validate

    Returns:
        bool: True if description is valid, False otherwise
    """

    return isinstance(description, str) and 1 <= len(description) <= 15


def is_valid_type(type_):
    """
    Parameters:
        type_ (str): type to validate

    Returns:
        bool: True if type is valid, False otherwise
    """

    return type_ in {"goal", "routine"}


def is_valid_frequency(frequency):
    """
    Parameters:
        frequency (str): frequency to validate

    Returns:
        bool: True if frequency is valid, False otherwise
    """

    return frequency in {"day", "week", "month", "year"}


def is_valid_rschedule(rschedule, frequency):
    """
    Parameters:
        rschedule (list): rschedule to validate
        frequency (str): frequency of rschedule

    Returns:
        bool: True if rschedule is valid, False otherwise

    Raises:
        ValueError: if frequency is not valid
    """

    if not is_valid_frequency(frequency):
        raise ValueError("frequency is not valid")

    if not isinstance(rschedule, list):
        return False

    frequency_max_day = {"day": 0, "week": 6, "month": 27, "year": 364}

    for spec in rschedule:
        if not (isinstance(spec, list) and len(spec) == 2 and
                isinstance(spec[0], int) and isinstance(spec[1], int) and
                0 <= spec[0] <= frequency_max_day[frequency] and
                0 <= spec[1] <= 24 * 60):
            return False

    return True


def is_valid_gschedule(gschedule, start_date, deadline):
    """
    Parameters:
        gschedule (list): gschedule to validate
        start_date (str)
        deadline (str)

    Returns:
        bool: True if gschedule is valid, False otherwise
    """

    if not isinstance(gschedule, list):
        return False

    for spec in gschedule:
        if not (isinstance(spec, list) and len(spec) == 2 and
                isinstance(spec[0], str) and isinstance(spec[1], int) and
                is_iso_date(spec[0]) and 0 <= spec[1] <= 24 * 60):
            return False
        if datetime.fromisoformat(spec[0]) < datetime.fromisoformat(start_date) or datetime.fromisoformat(spec[0]) > datetime.fromisoformat(deadline):
            return False

    return True


def is_valid_dates(start_date, deadline):
    """
    Parameters:
        start_date (str): start date to validate
        deadline (str): deadline to validate

    Returns:
        bool: True if dates are valid, False otherwise
    """

    if not (is_iso_date(start_date) and is_iso_date(deadline)):
        return False

    return datetime.fromisoformat(start_date) <= datetime.fromisoformat(deadline)


def is_iso_date(date_string):
    """
    Parameters:
        date_string (str): date string to validate

    Returns:
        bool: True if date string is valid, False otherwise
    """

    if not isinstance(date_string, str):
        return False

    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


def is_valid_rschedule_string(rschedule_string, frequency):
    """
    Validates if the given rschedule string can be converted to a valid rschedule list.

    Parameters:
        rschedule_string (str): The rschedule string to validate.
        frequency (str): The frequency of the rschedule.

    Returns:
        bool: True if the rschedule string is valid, False otherwise.
    """

    try:
        rschedule = json.loads(rschedule_string)
        return is_valid_rschedule(rschedule, frequency)
    except (json.JSONDecodeError, ValueError):
        return False


def is_valid_gschedule_string(gschedule_string, start_date, deadline):
    """
    Validates if the given gschedule string can be converted to a valid gschedule list.

    Parameters:
        gschedule_string (str): The gschedule string to validate.

    Returns:
        bool: True if the gschedule string is valid, False otherwise.
    """

    try:
        gschedule = json.loads(gschedule_string)
        return is_valid_gschedule(gschedule, start_date, deadline)
    except (json.JSONDecodeError, ValueError):
        return False


def get_new_item():
    """
    Gets a new item from the user with valid input.

    Returns:
        dict: A valid item dictionary.
    """

    description = prompt_for_value(
        "Enter description (1-15 characters): ", is_valid_description, "Invalid description.")
    type_ = prompt_for_value(
        "Enter type (goal or routine): ", is_valid_type, "Invalid type.")

    item = {
        "description": description,
        "type": type_
    }

    if type_ == "goal":
        start_date = prompt_for_value(
            "Enter start date (YYYY-MM-DD): ", is_iso_date, "Invalid start date.")
        deadline = prompt_for_value("Enter deadline (YYYY-MM-DD): ", lambda d: is_iso_date(
            d) and is_valid_dates(start_date, d), "Invalid deadline.")
        gschedule = prompt_for_value("Enter gschedule as a list of lists (e.g. [['2020-01-01', 30], ['2020-01-03', 45]]): ", lambda s: is_valid_gschedule_string(
            s, start_date, deadline), "Invalid gschedule.")
        item["start_date"] = start_date
        item["deadline"] = deadline
        item["gschedule"] = json.loads(gschedule)
    elif type_ == "routine":
        frequency = prompt_for_value(
            "Enter frequency (day, week, month, or year): ", is_valid_frequency, "Invalid frequency.")
        rschedule = prompt_for_value("Enter rschedule as a list of lists (e.g. [[1, 30], [3, 45]]): ", lambda s: is_valid_rschedule_string(
            s, frequency), "Invalid rschedule.")
        item["frequency"] = frequency
        item["rschedule"] = json.loads(rschedule)

    return item


def prompt_for_value(prompt_text, validation_func, error_message):
    """
    Prompts the user for input, validates it, and returns the value if valid.

    Parameters:
        prompt_text (str): The text to display when prompting the user.
        validation_func (function): A function that takes a single argument and returns a boolean.
        error_message (str): The error message to display if validation fails.

    Returns:
        Any: The user's input after validation.
    """

    while True:
        value = input(prompt_text)
        if validation_func(value):
            return value
        else:
            print(error_message)


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


def display_items(items):
    """
    Displays the items in a readable format.

    Parameters:
        items (list): A list of item dictionaries.

    Raises:
        ValueError: if items is not valid
    """

    if not items:
        print("No items in the list.")
        return

    if not is_valid_items(items):
        raise ValueError("Items is not valid")

    print("=== Items ===")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['description']} ({item['type']})")

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
    if not is_iso_date(date_str):
        raise ValueError("Date is not valid")

    items = get_items_for_date(data, date_str)
    print(f"=== {date_str} ===")
    display_items(items)


def get_items_for_date(data, date_str):
    """
    Parameters:
        data (dict): The data to get items from.
        date (str): The date to get items for.

    Returns:
        list: A list of item dictionaries.

    Raises:
        ValueError: if data is not valid
        ValueError: if date is not valid
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")
    if not is_iso_date(date_str):
        raise ValueError("Date is not valid")

    items = []

    for item in data["items"]:
        if item["type"] == "goal":
            if date_in_gschedule(item["gschedule"], date_str):
                items.append(item)
        elif item["type"] == "routine":
            if date_in_rschedule(item["frequency"], item["rschedule"], date_str):
                items.append(item)

    return items


def date_in_gschedule(gschedule, date_str):
    """
    Parameters:
        gschedule (list): A list of lists containing a date and time.
        date (str): The date to check.

    Returns:
        bool: True if the date is in the gschedule, False otherwise.

    Raises:
        ValueError: if date is not valid
    """

    if not is_iso_date(date_str):
        raise ValueError("Date is not valid")

    for item in gschedule:
        if item[0] == date_str:
            return True

    return False


def date_in_rschedule(frequency, rschedule, date_str):
    """
    Parameters:
        frequency (str): The frequency of the rschedule.
        rschedule (list): A list of lists containing a time.
        date (str): The date to check.

    Returns:
        bool: True if the date is in the rschedule, False otherwise.

    Raises:
        ValueError: if frequency is not valid
        ValueError: if rschedule is not valid
        ValueError: if date is not valid
    """

    if not is_valid_frequency(frequency):
        raise ValueError("frequency is not valid")
    if not is_valid_rschedule(rschedule, frequency):
        raise ValueError("rschedule is not valid")
    if not is_iso_date(date_str):
        raise ValueError("Date is not valid")

    if frequency == "day":
        return True

    if frequency == "week":
        day = get_day_of_week(date_str)
        for item in rschedule:
            if item[0] == day:
                return True

    if frequency == "month":
        day = int(date_str.split("-")[2])
        for item in rschedule:
            if item[0] == day:
                return True

    if frequency == "year":
        day = get_day_of_year(date_str)
        for item in rschedule:
            if item[0] == day:
                return True

    return False


def get_day_of_week(date_str):
    """
    Parameters:
        date (str): The date to get the day of the week for.

    Returns:
        int: The day of the week (0-6).

    Raises:
        ValueError: if date is not valid
    """

    if not is_iso_date(date_str):
        raise ValueError("Date is not valid")

    year = int(date_str.split("-")[0])
    month = int(date_str.split("-")[1])
    day = int(date_str.split("-")[2])

    return date(year, month, day).weekday()


def get_day_of_year(date_):
    """
    Parameters:
        date (str): The date to get the day of the year for.

    Returns:
        int: The day of the year (1-366).

    Raises:
        ValueError: if date is not valid
    """

    if not is_iso_date(date_):
        raise ValueError("Date is not valid")

    year = int(date_.split("-")[0])
    month = int(date_.split("-")[1])
    day = int(date_.split("-")[2])

    return datetime.date(year, month, day).timetuple().tm_yday


def display_controls():
    print('''
    =============== Controls ===============
    m - next day
    n - previous day
    mm - next week
    nn - previous week
    mmm - next month
    nnn - previous month
    mmmm - next year
    nnnn - previous year
    ? - display controls
    q - quit

    ''')


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


def main():
    data = retrieve_data()

    while True:
        choice = input("Enter choice or '?' for controls: ")
        if choice == '?':
            display_controls()
        elif choice == 'a':
            new_item = get_new_item()
            add_item(data, new_item)
            print("Item added successfully.")
        elif choice == 'd':
            display_items(data['items'])
        elif choice == 's':
            date = prompt_for_value(
                'Enter date (YYYY-MM-DD): ', is_iso_date, 'Date is not valid')
            display_items_for_date(data, date)
        elif choice == 'q':
            quit_program(data)
        else:
            print('Invalid choice')


main()
