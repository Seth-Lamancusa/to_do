import json
from datetime import date


VALID_ITEM_ATTRIBUTES = [
    "description",
    "type",
    "active",
    "rschedule",
    "frequency",
    "gschedule",
    "start_date",
    "deadline",
]
VALID_FREQUENCIES = ["day", "week", "month", "year"]
VALID_WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
VALID_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
WEEKDAY_TO_INT = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


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


# Validation functions for data dictionary


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


# Validation functions for item dictionary


def is_valid_item(item):
    """
    Parameters:
        item (dict): item to validate

    Returns:
        bool: True if item is valid, False otherwise
    """

    if not isinstance(item, dict):
        return False

    keys = {"description", "type", "active"}
    try:
        if item.get("type") == "goal":
            keys.update({"start_date", "deadline", "gschedule"})
        elif item.get("type") == "routine":
            keys.update({"frequency", "rschedule"})
        else:
            return False
    except KeyError:
        return False

    if set(keys) != set(item.keys()):
        return False

    if not (
        is_valid_description(item["description"])
        and is_valid_type(item["type"])
        and is_valid_active(item["active"])
    ):
        return False

    if item["type"] == "goal":
        return (
            is_valid_gschedule(item["gschedule"])
            and is_valid_date(item["start_date"])
            and is_valid_date(item["deadline"])
            and goal_attribute_values_compatible(
                item["gschedule"], item["start_date"], item["deadline"]
            )
        )
    elif item["type"] == "routine":
        return (
            is_valid_frequency(item["frequency"])
            and is_valid_rschedule(item["rschedule"])
            and routine_attribute_values_compatible(
                item["rschedule"], item["frequency"]
            )
        )


def routine_attribute_values_compatible(rschedule, frequency):
    """
    Parameters:
        rschedule (list): rschedule to validate
        frequency (str): frequency to validate

    Returns:
        bool: True if rschedule is compatible with frequency, False otherwise
    """

    if not is_valid_rschedule(rschedule):
        return False
    if not is_valid_frequency(frequency):
        return False

    if frequency == "day":
        return all([spec[0] == 0 for spec in rschedule])
    elif frequency == "week":
        return all([spec[0] in {0, 1, 2, 3, 4, 5, 6} for spec in rschedule])
    elif frequency == "month":
        return all([spec[0] in range(0, 28) for spec in rschedule])
    elif frequency == "year":
        return all([spec[0] in range(0, 365) for spec in rschedule])
    else:
        return False


def goal_attribute_values_compatible(gschedule, start_date, deadline):
    """
    Parameters:
        gschedule (list): gschedule to validate
        start_date (datetime.date): start date to validate
        deadline (datetime.date): deadline to validate

    Returns:
        bool: True if gschedule is compatible with start date and deadline, False otherwise
    """

    if not is_valid_gschedule(gschedule):
        return False

    return all(
        [start_date <= date.fromisoformat(spec[0]) <= deadline for spec in gschedule]
    )


def item_attribute_values_compatible(**kwargs):
    """
    Parameters:
        kwargs (dict): keyword arguments to validate

    Returns:
        bool: True if keyword arguments are compatible, False otherwise
    """

    if frozenset(kwargs.keys()) not in {
        frozenset({"gschedule", "start_date", "deadline"}),
        frozenset(
            {
                "rschedule",
                "frequency",
            }
        ),
    }:
        print(kwargs.keys())
        raise ValueError("Invalid arguments")

    if "gschedule" in kwargs:
        return goal_attribute_values_compatible(
            kwargs["gschedule"], kwargs["start_date"], kwargs["deadline"]
        )
    elif "rschedule" in kwargs:
        return routine_attribute_values_compatible(
            kwargs["rschedule"], kwargs["frequency"]
        )


# Validation functions for item keys


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


def is_valid_rschedule(rschedule):
    """
    Parameters:
        rschedule (list): rschedule to validate

    Returns:
        bool: True if rschedule is valid in isolation, False otherwise

    Raises:
        ValueError: if frequency is not valid
    """

    if not isinstance(rschedule, list):
        return False

    for spec in rschedule:
        if not (
            isinstance(spec, list)
            and len(spec) == 2
            and isinstance(spec[0], int)
            and isinstance(spec[1], int)
            and 0 <= spec[1] <= 24 * 60
        ):
            return False

    return True


def is_valid_frequency(frequency):
    """
    Parameters:
        frequency (str): frequency to validate

    Returns:
        bool: True if frequency is valid, False otherwise
    """

    return frequency in VALID_FREQUENCIES


def is_valid_gschedule(gschedule):
    """
    Parameters:
        gschedule (list): gschedule to validate

    Returns:
        bool: True if gschedule is valid, False otherwise
    """

    if not isinstance(gschedule, list):
        return False

    for spec in gschedule:
        if not (
            isinstance(spec, list)
            and len(spec) == 2
            and isinstance(spec[0], date)
            and isinstance(spec[1], int)
            and 0 <= spec[1] <= 24 * 60
        ):
            return False

    return True


def is_valid_date(date_):
    """
    Parameters:
        date_ (datetime.date): date to validate

    Returns:
        bool: True if date is valid, False otherwise
    """

    return isinstance(date_, date)


def is_valid_iso_date(date_string):
    """
    Parameters:
        date_string (str): date string to validate

    Returns:
        bool: True if date string is valid, False otherwise
    """

    if not isinstance(date_string, str):
        return False

    try:
        date.fromisoformat(date_string)
        return True
    except ValueError:
        return False


def is_valid_active(active):
    """
    Parameters:
        active (bool): active to validate

    Returns:
        bool: True if active is valid, False otherwise
    """

    return isinstance(active, bool)


# User input validation functions


def is_valid_attribute_key(attribute):
    """
    Parameters:
        attribute (str): The attribute to check.

    Returns:
        bool: True if the attribute is valid, False otherwise.
    """

    return attribute in VALID_ITEM_ATTRIBUTES


def is_valid_attribute_value(attribute, value):
    """
    Parameters:
        attribute (str): The attribute to check.
        value (str): The value to check.

    Returns:
        bool: True if the value is valid, False otherwise.
    """

    if attribute == "description":
        return is_valid_description(value)
    elif attribute == "type":
        return is_valid_type(value)
    elif attribute == "active":
        return is_valid_active(value)
    elif attribute == "rschedule":
        return is_valid_rschedule(json.loads(value))
    elif attribute == "frequency":
        return is_valid_frequency(value)
    elif attribute == "gschedule":
        return is_valid_gschedule(value)
    elif attribute == "start_date":
        return is_valid_date(value)
    elif attribute == "deadline":
        return is_valid_date(value)
    else:
        return False


def is_valid_rschedule_string(rschedule_string):
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
        return is_valid_rschedule(rschedule)
    except (json.JSONDecodeError, ValueError):
        return False


def is_valid_gschedule_string(gschedule_string):
    """
    Validates if the given gschedule string can be converted to a valid gschedule list.

    Parameters:
        gschedule_string (str): The gschedule string to validate.

    Returns:
        bool: True if the gschedule string is valid, False otherwise.
    """

    try:
        gschedule = json.loads(gschedule_string)
        return is_valid_gschedule(gschedule)
    except (json.JSONDecodeError, ValueError):
        return False


def is_valid_duration(duration):
    """
    Parameters:
        time (int): time to validate

    Returns:
        bool: True if time is valid duration, False otherwise
    """

    return 0 <= duration <= 24 * 60


def is_valid_weekday(weekday):
    """
    Parameters:
        weekday (str): weekday to validate

    Returns:
        bool: True if weekday is valid, False otherwise
    """

    return weekday in VALID_WEEKDAYS


def is_valid_month_day(month_day):
    """
    Parameters:
        month_day (int): month_day to validate

    Returns:
        bool: True if month_day is valid, False otherwise
    """

    return month_day < 29


def is_valid_month(month):
    """
    Parameters:
        month (str): month to validate

    Returns:
        bool: True if month is valid, False otherwise
    """

    return month in VALID_MONTHS
