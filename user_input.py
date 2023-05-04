from datetime import date
from validation import *
from helpers import *


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


def prompt_for_new_item(data):
    """
    Gets a new item from the user with valid input.

    Parameters:
        data (dict): The data to validate against.

    Returns:
        dict: A valid item dictionary.
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")

    while True:
        description = prompt_for_new_item_desc(data)
        type_ = prompt_for_valid_item_attribute_value("type")

        item = {
            "description": description,
            "type": type_,
            "active": True,
        }

        if type_ == "goal":
            start_date = prompt_for_valid_item_attribute_value("start_date")
            deadline = prompt_for_valid_item_attribute_value("deadline")
            gschedule = prompt_for_valid_item_attribute_value("gschedule")
            item["start_date"] = start_date
            item["deadline"] = deadline
            item["gschedule"] = gschedule
        elif type_ == "routine":
            frequency = prompt_for_valid_item_attribute_value("frequency")
            rschedule = prompt_for_valid_item_attribute_value("rschedule")
            item["frequency"] = frequency
            item["rschedule"] = json.loads(rschedule)

        if is_valid_item(item):
            return item
        else:
            print("Incompatible item attributes.")


def prompt_for_new_item_desc(data):
    """
    Parameters:
        data (dict): The data with which to compare item desc.

    Returns:
        str: A description for a new item.

    Raises:
        ValueError: If the data is invalid.
    """

    if not is_valid_data(data):
        raise ValueError("Invalid data.")

    return prompt_for_value(
        "Enter item description: ",
        lambda i: is_valid_description(i) and not item_in_data(data, i),
        "Item is invalid or already exists.",
    )


def prompt_for_existing_item_desc(data):
    """
    Parameters:
        data (dict): The data to get an item from.

    Returns:
        str: A description for an existing item.

    Raises:
        ValueError: If the data is invalid.
    """

    if not is_valid_data(data):
        raise ValueError("Invalid data.")

    return prompt_for_value(
        "Enter item description: ",
        lambda i: is_valid_description(i) and item_in_data(data, i),
        "Item is invalid or does not exist.",
    )


def prompt_for_valid_date():
    """
    Returns:
        datetime.date: A valid date in the format YYYY-MM-DD.
    """

    return date.fromisoformat(
        prompt_for_value("date", is_valid_iso_date, "Invalid date")
    )


def prompt_for_valid_item_attribute_value(attribute):
    """
    Parameters:
        attribute (str): The attribute to get from the user.

    Returns:
        any: A valid attribute value.
    """

    if attribute == "desc":
        return prompt_for_value(
            "Enter valid description: ", is_valid_description, "Invalid description."
        )
    elif attribute == "type":
        return prompt_for_value("Enter valid type: ", is_valid_type, "Invalid type.")
    elif attribute == "active":
        return prompt_for_value(
            "Enter valid active status: ", is_valid_active, "Invalid active status."
        )
    elif attribute == "rschedule":
        return json.loads(
            prompt_for_value(
                "Enter valid rschedule: ",
                is_valid_rschedule_string,
                "Invalid rschedule.",
            )
        )
    elif attribute == "frequency":
        return prompt_for_value(
            "Enter valid frequency: ", is_valid_frequency, "Invalid frequency."
        )
    elif attribute == "gschedule":
        return json.loads(
            prompt_for_value(
                "Enter valid gschedule: ",
                is_valid_gschedule_string,
                "Invalid gschedule.",
            )
        )
    elif attribute == "start_date":
        return date.fromisoformat(
            prompt_for_value(
                "Enter valid start date: ",
                is_valid_iso_date,
                "Invalid start date.",
            )
        )
    elif attribute == "deadline":
        return date.fromisoformat(
            prompt_for_value(
                "Enter valid deadline: ",
                is_valid_iso_date,
                "Invalid deadline.",
            )
        )
    else:
        raise ValueError("Invalid attribute.")


def prompt_for_compatible_item_attribute_value(attribute, **kwargs):
    """
    Parameters:
        attribute (str): The attribute to get from the user.
        **kwargs: Attributes and values to check validity against.

    Returns:
        any: A valid attribute value.
    """

    if frozenset(kwargs.keys()) not in {
        frozenset({"frequency"}),
        frozenset({"rschedule"}),
        frozenset({"gschedule", "start_date"}),
        frozenset({"gschedule", "deadline"}),
        frozenset({"start_date", "deadline"}),
    }:
        raise ValueError("Invalid arguments.")

    while True:
        value = prompt_for_valid_item_attribute_value(attribute)
        kwargs[attribute] = value
        if item_attribute_values_compatible(**kwargs):
            return value
        else:
            print("Incompatible item attribute values.")


def prompt_for_existing_item_attribute(item):
    """
    Parameters:
        item (dict): The item test the attribute against

    Returns:
        str: The attribute

    Raises:
        ValueError: if item is not valid
    """

    if not is_valid_item(item):
        raise ValueError("item is not valid")

    return prompt_for_value(
        f"Enter existing attribute for {item['description']}: ",
        lambda i: is_valid_attribute_key(i) and i in item,
        f"Invalid or non-existent attribute for {item['description']}",
    )


def prompt_for_rschedule(frequency):
    """
    Parameters:
        frequency (str): The frequency to get an rschedule for.

    Returns:
        list: A valid rschedule for the frequency.

    Raises:
        ValueError: if frequency is not valid
    """

    if not is_valid_frequency(frequency):
        raise ValueError("frequency is not valid")

    rschedule = []
    while True:
        if frequency == "day":
            time = prompt_for_value(
                "Enter duration: ", is_valid_duration, "Invalid duration."
            )
            rschedule.append([0, time])
        elif frequency == "week":
            day = prompt_for_value(
                "Enter weekday: ", is_valid_weekday, "Invalid weekday."
            )
            duration = prompt_for_value(
                "Enter duration: ", is_valid_duration, "Invalid duration."
            )
            rschedule.append([WEEKDAY_TO_INT[day], duration])
        elif frequency == "month":
            day = prompt_for_value(
                "Enter day of month: ",
                is_valid_month_day,
                "Invalid day of month (please choose day < 29).",
            )
            duration = prompt_for_value(
                "Enter duration: ", is_valid_duration, "Invalid duration."
            )
            rschedule.append([day - 1, duration])
        elif frequency == "year":
            date_ = prompt_for_value(
                "Enter date in ISO format: ", is_valid_iso_date, "Invalid date."
            )
            duration = prompt_for_value(
                "Enter duration: ", is_valid_duration, "Invalid duration."
            )
            rschedule.append([get_day_of_year(date_), duration])
