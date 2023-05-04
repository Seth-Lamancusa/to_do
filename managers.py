from validation import *
from helpers import *


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
        item_desc (str): The description of the item to delete.

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
        item_desc (str): The description of the item to edit.
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
        raise ValueError("data is not valid")
    if not is_valid_description(item_desc):
        raise ValueError("item_desc is not valid")
    if not is_valid_attribute_key(attribute):
        raise ValueError("attribute is not valid")
    if not is_valid_attribute_value(attribute, new_value):
        raise ValueError("new_value is not valid")
    compat = get_compatibility_dict(get_item(item_desc, data))
    del compat[attribute]
    compat[attribute] = new_value
    if not item_attribute_values_compatible(**compat):
        raise ValueError("new_value is not compatabile with attribute")
    if item_desc not in [item["description"] for item in data["items"]]:
        raise ValueError("item_desc is not in data")

    for item in data["items"]:
        if item["description"] == item_desc:
            item[attribute] = new_value
