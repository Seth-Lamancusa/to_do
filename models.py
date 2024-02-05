import datetime
import json


# Data is a dictionary containing exactly 1 key: "items"
class UserData:
    def __init__(self, data):
        self.validate_data(data)
        self.items = data["items"]

    def validate_data(self, data):
        if not isinstance(data, dict) or len(data) != 1 or "items" not in data:
            raise ValueError("Invalid data")
        for item in data["items"]:
            if not isinstance(item, Item):
                raise ValueError("Invalid item")

    def write_data_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump({"items": self.items}, file)


class Item:
    descriptions = set()  # To track all descriptions

    def __init__(
        self,
        description,
        item_type,
        active,
        rschedule=None,
        frequency=None,
        gschedule=None,
        start_date=None,
        deadline=None,
    ):
        self.validate_description(description)
        self.description = description
        self.validate_type(item_type)
        self.type = item_type
        self.validate_active(active)
        self.active = active

        if item_type == "routine":
            self.validate_routine(frequency, rschedule)
            self.frequency = frequency
            self.rschedule = rschedule
        elif item_type == "goal":
            self.validate_goal(gschedule, start_date, deadline)
            self.gschedule = gschedule
            self.start_date = start_date
            self.deadline = deadline

        self.descriptions.add(description)

    # Validation methods

    @classmethod
    def validate_description(cls, description):
        if not 1 <= len(description) <= 15 or description in cls.descriptions:
            raise ValueError("Invalid or duplicate description.")

    def validate_type(self, item_type):
        if item_type not in {"routine", "goal"}:
            raise ValueError("Invalid item type.")

    def validate_active(self, active):
        if not isinstance(active, bool):
            raise ValueError("Invalid active status.")

    # rschedule and gschedule can be validated in isolation, but routine and goal validation depend on cominations of item attributes being compatible

    def validate_routine(self, frequency, rschedule):
        self.validate_frequency(frequency)
        self.validate_rschedule(rschedule)

        if frequency == "day":
            if not all([spec[0] == 0 for spec in rschedule]):
                raise ValueError("Invalid rschedule")
        elif frequency == "week":
            if not all([spec[0] in {0, 1, 2, 3, 4, 5, 6} for spec in rschedule]):
                raise ValueError("Invalid rschedule")
        elif frequency == "month":
            if not all([spec[0] in range(0, 28) for spec in rschedule]):
                raise ValueError("Invalid rschedule")
        elif frequency == "year":
            if not all([spec[0] in range(0, 365) for spec in rschedule]):
                raise ValueError("Invalid rschedule")

    def validate_goal(self, gschedule, start_date, deadline):
        self.validate_gschedule(gschedule)
        self.validate_date(start_date)
        self.validate_date(deadline)

        if not all([start_date <= spec[0] <= deadline for spec in gschedule]):
            raise ValueError("Invalid gschedule")

    # Internal validation helpers

    def validate_gschedule(self, gschedule):
        if not isinstance(gschedule, list):
            raise ValueError("Invalid gschedule")

        for spec in gschedule:
            if not (
                isinstance(spec, list)
                and len(spec) == 2
                and isinstance(spec[0], datetime.date)
                and isinstance(spec[1], int)
                and 0 <= spec[1] <= 24 * 60
            ):
                raise ValueError("Invalid gschedule")

    def validate_rschedule(self, rschedule):
        if not isinstance(rschedule, list):
            raise ValueError("Invalid rschedule")

        for spec in rschedule:
            if not (
                isinstance(spec, list)
                and len(spec) == 2
                and isinstance(spec[0], int)
                and isinstance(spec[1], int)
                and 0 <= spec[1] <= 24 * 60
            ):
                raise ValueError("Invalid rschedule")

    def validate_date(self, date):
        if not isinstance(date, datetime.date):
            raise ValueError("Invalid date")

    def validate_frequency(self, frequency):
        if frequency not in ["day", "week", "month", "year"]:
            raise ValueError("Invalid frequency")
