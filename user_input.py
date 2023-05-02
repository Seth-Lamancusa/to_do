from validation import *


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


def prompt_for_new_item():
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
        "type": type_,
        "active": True,
    }

    if type_ == "goal":
        start_date = prompt_for_value(
            "Enter start date (YYYY-MM-DD): ", is_valid_iso_date, "Invalid start date.")
        deadline = prompt_for_value("Enter deadline (YYYY-MM-DD): ", lambda d: is_valid_iso_date(
            d) and is_valid_iso_date(start_date, d), "Invalid deadline.")
        gschedule = prompt_for_value("Enter gschedule as a list of lists (e.g. [[\"2020-01-01\", 30], [\"2020-01-03\", 45]]): ", lambda s: is_valid_gschedule_string(
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


def prompt_for_valid_date():
    """
    Returns:
        str: A valid date in the format YYYY-MM-DD.
    """

    prompt_for_value("date", is_valid_iso_date, "Invalid date")


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
        "Enter item description: ", lambda i: is_valid_description(i) and item_in_data(data, i), "Item is invalid or does not exist.")


def prompt_for_existing_attribute(item):
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

    return prompt_for_value(f"Enter existing attribute for {item['description']}: ", lambda i: is_valid_attribute_key(
        i) and i in item, f"Invalid or non-existent attribute for {item['description']}")


def prompt_for_valid_attribute_value(attribute, item):
    """
    Parameters:
        attribute (str): The attribute to get a value for.
        item (dict): The item to get a value for.

    Returns:
        str: A valid value for the attribute.

    Raises:
        ValueError: if attribute is not valid
    """

    if not is_valid_attribute_key(attribute):
        raise ValueError("attribute is not valid")

    if attribute == "description":
        return prompt_for_value("Enter new description: ", is_valid_description, "Invalid description.")
    elif attribute == "type":
        return prompt_for_value("Enter new type: ", is_valid_type, "Invalid type.")
    elif attribute == "active":
        return prompt_for_value("Enter new active status: ", is_valid_active, "Invalid active status.")
    elif attribute == "rschedule":
        return prompt_for_value("Enter new rschedule: ", lambda i: is_valid_rschedule_string(i, item["frequency"]), "Invalid rschedule.")
    elif attribute == "frequency":
        return prompt_for_value("Enter new frequency: ", is_valid_frequency, "Invalid frequency.")
    elif attribute == "gschedule":
        return prompt_for_value("Enter new gschedule: ", is_valid_gschedule, "Invalid gschedule.")
    else:
        return prompt_for_value("Enter new date: ", is_valid_iso_date, "Invalid date.")
