from datetime import date, timedelta
from validation import *
from helpers import *


CANCEL = "cancel"


def prompt_for_value(prompt_text, validation_func, error_message):
    """
    Prompts the user for input, validates it, and returns the value if valid.

    Parameters:
        prompt_text (str): The text to display when prompting the user.
        validation_func (function): A function that takes a single argument and returns a boolean.
        error_message (str): The error message to display if validation fails.

    Returns:
        Any: The user's input after validation or
        None.
    """

    while True:
        value = input(prompt_text)
        if value == CANCEL:
            print("Operation cancelled by user.")
            return None
        elif validation_func(value):
            return value
        else:
            print(error_message)


def prompt_for_new_item(data):
    """
    Gets a new item from the user with valid input.

    Parameters:
        data (dict): The data to validate against.

    Returns:
        dict: A valid item dictionary or
        None.
    """

    if not is_valid_data(data):
        raise ValueError("Data is not valid")

    while True:
        description = prompt_for_new_item_desc(data)
        type_ = prompt_for_valid_item_attribute_value("type")
        if description is None or type_ is None:
            return None

        item = {
            "description": description,
            "type": type_,
            "active": True,
        }

        if type_ == "goal":
            start_date = prompt_for_valid_item_attribute_value("start_date")
            deadline = prompt_for_valid_item_attribute_value("deadline")
            gschedule = prompt_for_gschedule(start_date, deadline)
            if start_date is None or deadline is None or gschedule is None:
                return None
            item["start_date"] = start_date
            item["deadline"] = deadline
            item["gschedule"] = gschedule
        elif type_ == "routine":
            frequency = prompt_for_valid_item_attribute_value("frequency")
            rschedule = prompt_for_rschedule(frequency)
            if frequency is None or rschedule is None:
                return None
            item["frequency"] = frequency
            item["rschedule"] = rschedule

        if is_valid_item(item):
            return item
        else:
            print("Incompatible item attributes.")


def prompt_for_new_item_desc(data):
    """
    Parameters:
        data (dict): The data with which to compare item desc.

    Returns:
        str: A description for a new item or
        None.

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
        str: A description for an existing item or
        None.

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
        datetime.date: A valid date in the format YYYY-MM-DD or
        None.
    """

    date_string = prompt_for_value("date", is_valid_iso_date, "Invalid date")
    if date_string is None:
        return None
    return date.fromisoformat(date_string)


def prompt_for_valid_item_attribute_value(attribute):
    """
    Parameters:
        attribute (str): The attribute to get from the user.

    Returns:
        any: A valid attribute value or
        None.
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
        rschedule_string = prompt_for_value(
            "Enter valid rschedule: ",
            is_valid_rschedule_string,
            "Invalid rschedule.",
        )
        if rschedule_string is None:
            return None
        return json.loads(rschedule_string)
    elif attribute == "frequency":
        return prompt_for_value(
            "Enter valid frequency: ", is_valid_frequency, "Invalid frequency."
        )
    elif attribute == "gschedule":
        gschedule_string = prompt_for_value(
            "Enter valid gschedule: ",
            is_valid_gschedule_string,
            "Invalid gschedule.",
        )
        if gschedule_string is None:
            return None
        return json.loads(gschedule_string)
    elif attribute == "start_date":
        date_string = prompt_for_value(
            "Enter valid start date: ",
            is_valid_iso_date,
            "Invalid start date.",
        )
        if date_string is None:
            return None
        return date.fromisoformat(date_string)
    elif attribute == "deadline":
        date_string = prompt_for_value(
            "Enter valid deadline: ",
            is_valid_iso_date,
            "Invalid deadline.",
        )
        if date_string is None:
            return None
        return date.fromisoformat(date_string)
    else:
        raise ValueError("Invalid attribute.")


def prompt_for_compatible_item_attribute_value(attribute, **kwargs):
    """
    Parameters:
        attribute (str): The attribute to get from the user.
        **kwargs: Attributes and values to check compatibility against.

    Returns:
        any: A valid attribute value or
        None.
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
        if value is None:
            return None
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
        str: The attribute or
        None.

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
        list: A valid rschedule for the frequency or
        None.

    Raises:
        ValueError: if frequency is not valid
    """

    if not is_valid_frequency(frequency):
        raise ValueError("frequency is not valid")

    rschedule = []
    while True:
        if frequency == "day":
            duration_string = prompt_for_value(
                "Enter duration: ", is_valid_duration_string, "Invalid duration."
            )
            if duration_string is None:
                return None
            duration = int(duration_string)
            rschedule.append([0, duration])
        elif frequency == "week":
            day = prompt_for_value(
                "Enter weekday: ", is_valid_weekday, "Invalid weekday."
            )
            duration_string = prompt_for_value(
                "Enter duration: ", is_valid_duration_string, "Invalid duration."
            )
            if duration_string is None or day is None:
                return None
            duration = int(duration_string)
            rschedule.append([WEEKDAY_TO_INT[day], duration])
        elif frequency == "month":
            day = prompt_for_value(
                "Enter day of month: ",
                is_valid_month_day,
                "Invalid day of month (please choose day < 29).",
            )
            duration_string = prompt_for_value(
                "Enter duration: ", is_valid_duration_string, "Invalid duration."
            )
            if duration_string is None or day is None:
                return None
            duration = int(duration_string)
            rschedule.append([day - 1, duration])
        elif frequency == "year":
            date_string = prompt_for_value(
                "Enter date in ISO format: ", is_valid_iso_date, "Invalid date."
            )
            if date_string is None:
                return None
            date_ = date.fromisoformat(date_string)
            duration_string = prompt_for_value(
                "Enter duration: ", is_valid_duration_string, "Invalid duration."
            )
            if duration_string is None:
                return None
            duration = int(duration_string)
            rschedule.append([date_.timetuple().tm_yday, duration])
        t = prompt_for_value("Add another? (y/n): ", is_valid_yes_no, "Invalid input.")
        if t == None:
            return None
        if t == "n":
            return rschedule


def prompt_for_gschedule(start_date, deadline):
    """
    Parameters:
        start_date (datetime.date): The start date to get a gschedule for.
        deadline (datetime.date): The deadline to get a gschedule for.

    Returns:
        list: A valid gschedule for the start date and deadline.

    Raises:
        ValueError: if start_date or deadline are not valid
    """

    if not is_valid_date(start_date):
        raise ValueError("start_date is not valid")
    if not is_valid_date(deadline):
        raise ValueError("deadline is not valid")

    gschedule = []
    while True:
        i = prompt_for_value(
            "Do you want to enter a date, a positive int (days from today), or a negative int (days before deadline)? (d/p/n): ",
            lambda i: i in ["d", "p", "n"],
            "Invalid input.",
        )
        if i == None:
            return None
        elif i == "d":
            date_string = prompt_for_value(
                "Enter date in ISO format: ",
                lambda i: is_valid_iso_date(i)
                and start_date <= date.fromisoformat(i)
                and date.fromisoformat(i) <= deadline,
                "Invalid date.",
            )
            if date_string is None:
                return None
            date_ = date.fromisoformat(date_string)
        elif i == "p":
            date_string = prompt_for_value(
                "Enter a positive int (days after today): ",
                lambda i: "-" not in i
                and i.isdigit()
                and int(i) <= (deadline - date.today()).days,
                "Invalid non-negative int.",
            )
            if date_string is None:
                return None
            date_ = date.today() + timedelta(days=int(date_string))
        elif i == "n":
            date_string = prompt_for_value(
                "Enter a negative int (days before deadline): ",
                lambda i: "-" in i
                and i[1:].isdigit()
                and int(i[1:]) <= (deadline - date.today()).days,
                "Invalid non-positive int.",
            )
            if date_string is None:
                return None
            date_ = deadline + timedelta(days=int(date_string))
        duration_string = prompt_for_value(
            "Enter duration: ", is_valid_duration_string, "Invalid duration."
        )
        if duration_string is None:
            return None
        duration = int(duration_string)
        gschedule.append([date_, duration])
        t = prompt_for_value("Add another? (y/n): ", is_valid_yes_no, "Invalid input.")
        if t == None:
            return None
        if t == "n":
            return gschedule
