# **To-Documentation**

## **Data Validity**

* Data is a python dictionary containing exactly 1 keys: "items"
* Example:
```python
{
    "items": [
        {
            "description": "Meditate",
            "type": "routine",
            "frequency": "week",
            "schedule": [
                [
                    1,
                    15
                ],
                [
                    3,
                    15
                ],
                [
                    5,
                    15
                ]
            ]
        },
        {
            "description": "Read GEB",
            "type": "goal",
            "start_date": "2023-03-22",
            "deadline": "2023-08-22",
        }
    ]
}
```

### **items**

* for each item:
    * "frequency" and "schedule" values must be compatible
    * if present, "start_date" and "deadline" values must be compatible
* two items cannot have the same description
* The value for key "items" is a list of dictionaries with following keys (exhaustive):
    * "description"
        * string
        * Length: 1-15 characters
        * Simple description of item
    * "type"
        * string
        * "goal" or "routine"
        * Indicates whether item has deadline
    * "frequency" (only present if "type" has value "routine")
        * string
        * "day", "week", "month", or "year"
        * Task to be done at least once per frequency
    * "schedule" (only present if "type" has value "routine")
        * list
        * contains routine specifications (lists of 2 non-negative integers)
            * first integer is day of day, week (Monday is 0), month, or year of task
                * cannot exceed (minimum length of frequency in days) - 1 (0, 6, 27, 364)
                    * rationale here is that it's the easiest way to code it and it's a pretty rare case that one would *need* something on the last few days of the month
            * second integer is amount of time to be spent on task on that day in minutes
                * cannot exceed 24 * 60
    * "start_date" (only present if "type" has value "goal")
        * string
        * ISO formatted date on which goal is created
    * "deadline" (only present if "type" has value "goal")
        * string
        * ISO formatted date on which goal is to be completed
        * cannot be before start_date

