from todo import save_data
from models import UserData, Item
import json
from helpers import *
from managers import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date


with open("data.json", "r") as file:
    data = UserData(json.load(file))


class MainScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="todo")
        self.label.pack(fill="both", expand=True)

        self.frame_container = tk.Frame(self)
        self.frame_container.pack(fill="both", expand=True)

        # Set up two column layout
        self.day_view = tk.Frame(self.frame_container, bg="#d8f0e3")
        self.day_view.grid(row=0, column=0, sticky="nsew")

        self.menu = tk.Frame(self.frame_container, bg="#ddf0d8")
        self.menu.grid(row=0, column=1, sticky="nsew")

        # Create buttons on rhs
        self.add_button = tk.Button(
            self.menu, text=f"Add Item", command=self.master.show_add_screen
        )
        self.add_button.pack(pady=5)

        self.view_all_button = tk.Button(
            self.menu, text=f"View All Items", command=self.master.show_items_screen
        )
        self.view_all_button.pack(pady=5, padx=10)

        self.delete_button = tk.Button(
            self.menu, text=f"Delete Item", command=self.master.show_delete_screen
        )
        self.delete_button.pack(pady=5)

        self.edit_button = tk.Button(self.menu, text=f"Edit Item")
        self.edit_button.pack(pady=5)

        # Create text on lhs
        self.refresh_day_view()

        # Create exit button
        self.exit_button = tk.Button(
            self, text="Exit", command=self.master.on_closing, bg="#f0d8d8"
        )
        self.exit_button.pack(fill="both", expand=True)

    def refresh_day_view(self):
        # Clear the day_view frame
        for widget in self.day_view.winfo_children():
            widget.destroy()

        # Re-create the today label
        self.today_label = tk.Label(self.day_view, text=str(date.today()))
        self.today_label.pack(pady=5, padx=10)

        # Re-create the items for the current date
        self.item_list = get_items_for_date(data, date.today())
        for item in self.item_list:
            item_label = tk.Label(self.day_view, text=item["description"])
            item_label.pack(pady=5, padx=10)


class ItemsScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="All items")
        self.label.pack()

        self.menu_button = tk.Button(
            self, text="Go to Main Screen", command=self.master.show_main_screen
        )
        self.menu_button.pack()

        # Call refresh_items() after defining self.menu_button
        self.refresh_items()

    def refresh_items(self):
        # Clear the items frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget["text"] != "All items":
                widget.destroy()

        # Re-create the items
        for item in data.items:
            self.item_label = tk.Label(self, text=item.description)
            self.item_label.pack(padx=10, pady=5)

        # Delete and repack the button so it's at the bottom
        self.menu_button.pack_forget()
        self.menu_button.pack()


class DeleteScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.v = tk.StringVar(value=0)
        self.label = tk.Label(self, text="Select item to delete.")
        self.label.pack()
        self.select_button = tk.Button(self, text="Select", command=self.submit_action)
        self.select_button.pack()
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.master.show_main_screen
        )
        self.cancel_button.pack()

        self.refresh_items()

    def refresh_items(self):
        # Clear current Radiobuttons
        for widget in self.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.destroy()

        # Create Radiobuttons for items in the data
        for item in data.items:
            item_button = tk.Radiobutton(
                self,
                text=item.description,
                variable=self.v,
                value=item.description,
            )
            item_button.pack(padx=10, pady=5)

        # Delete and repack the submit and cancel buttons so at bottom
        self.select_button.pack_forget()
        self.cancel_button.pack_forget()
        self.select_button.pack()
        self.cancel_button.pack()

    def submit_action(self):
        # Delete item from data
        delete_item(data, self.v.get())
        self.master.show_main_screen()


class AddScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="Enter item to add.")
        self.label.pack()

        # Description Entry
        self.lbl_description = ttk.Label(self, text="Description")
        self.lbl_description.pack()
        self.entry_description = ttk.Entry(self)
        self.entry_description.pack()

        # Type Radio Buttons
        self.lbl_type = ttk.Label(self, text="Type")
        self.lbl_type.pack()
        self.type_var = tk.StringVar(value="goal")
        self.rbtn_goal = ttk.Radiobutton(
            self,
            text="Goal",
            variable=self.type_var,
            value="goal",
            command=self.show_frame,
        )
        self.rbtn_goal.pack()
        self.rbtn_routine = ttk.Radiobutton(
            self,
            text="Routine",
            variable=self.type_var,
            value="routine",
            command=self.show_frame,
        )
        self.rbtn_routine.pack()

        # Active Checkbox
        self.active_var = tk.IntVar(value=1)
        self.chk_active = ttk.Checkbutton(
            self, text="Active", variable=self.active_var, onvalue=1, offvalue=0
        )
        self.chk_active.pack()

        # Goal Frame
        self.goal_frame = ttk.Frame(self)
        self.lbl_start_date = ttk.Label(self.goal_frame, text="Start Date")
        self.lbl_start_date.pack()
        self.date_start = DateEntry(self.goal_frame)
        self.date_start.pack()
        self.lbl_deadline = ttk.Label(self.goal_frame, text="Deadline")
        self.lbl_deadline.pack()
        self.date_deadline = DateEntry(self.goal_frame)
        self.date_deadline.pack()

        # Frame for entering gschedule
        self.gschedule_frame = ttk.LabelFrame(
            self.goal_frame, text="Dates and Durations"
        )
        self.gschedule_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.first_row = GoalScheduleRow(
            self.gschedule_frame, self.date_start, self.date_deadline
        )
        self.first_row.pack(fill=tk.X, padx=5, pady=2)

        # Routine Frame
        self.routine_frame = ttk.Frame(self)
        self.frequency_label = ttk.Label(self, text="Frequency")
        self.frequency_label.pack()
        self.routine_var = tk.StringVar(value="daily")
        self.routine_var.trace_add("write", self.on_routine_frequency_change)
        self.rbtn_daily = ttk.Radiobutton(
            self.routine_frame, text="Daily", variable=self.routine_var, value="daily"
        )
        self.rbtn_daily.pack()
        self.rbtn_weekly = ttk.Radiobutton(
            self.routine_frame, text="Weekly", variable=self.routine_var, value="weekly"
        )
        self.rbtn_weekly.pack()
        self.rbtn_monthly = ttk.Radiobutton(
            self.routine_frame,
            text="Monthly",
            variable=self.routine_var,
            value="monthly",
        )
        self.rbtn_monthly.pack()
        self.rbtn_yearly = ttk.Radiobutton(
            self.routine_frame, text="Yearly", variable=self.routine_var, value="yearly"
        )
        self.rbtn_yearly.pack()

        # Frame for entering rschedule
        self.routine_schedule_frame = ttk.LabelFrame(
            self.routine_frame, text="Routine Schedule"
        )
        self.routine_schedule_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.first_routine_row = RoutineScheduleRow(
            self.routine_schedule_frame, self.routine_var
        )
        self.first_routine_row.pack(fill=tk.X, padx=5, pady=2)
        self.btn_cancel = ttk.Button(
            self, text="Cancel", command=self.master.show_main_screen
        )
        self.btn_submit = ttk.Button(self, text="Submit", command=self.submit_action)

        self.show_frame()

    def show_frame(self):
        # Show the appropriate frame based on the type selected
        if self.type_var.get() == "goal":
            self.goal_frame.pack()
            self.routine_frame.pack_forget()
        else:
            self.goal_frame.pack_forget()
            self.routine_frame.pack()

        # Repack the buttons so that they are at the bottom
        self.btn_cancel.pack_forget()
        self.btn_submit.pack_forget()
        self.btn_cancel.pack()
        self.btn_submit.pack()

    def on_routine_frequency_change(self, *args):
        # Clear existing rows
        for widget in self.routine_schedule_frame.winfo_children():
            widget.destroy()

        # Add a new row based on the new frequency
        new_row = RoutineScheduleRow(self.routine_schedule_frame, self.routine_var)
        new_row.pack(fill=tk.X, padx=5, pady=2)

    def submit_action(self):
        # Get the data from the widgets
        description = self.entry_description.get()
        type_selected = self.type_var.get()
        active = True if self.active_var.get() == 1 else False
        if type_selected == "goal":
            month, day, year = map(int, self.date_start.get().split("/"))
            start_date = datetime(year=2000 + year, month=month, day=day).date()
            month, day, year = map(int, self.date_deadline.get().split("/"))
            deadline = datetime(year=2000 + year, month=month, day=day).date()
            gschedule = []
            for child in self.gschedule_frame.winfo_children():
                if isinstance(child, GoalScheduleRow) and child.duration_entry.get():
                    month, day, year = map(int, child.date_picker.get().split("/"))
                    date_ = datetime(year=2000 + year, month=month, day=day).date()
                    duration = child.duration_entry.get()
                    gschedule.append([date_, int(duration)])
        else:
            freq_selected = self.routine_var.get()
            rschedule = []  # Routine schedule list
            for child in self.routine_schedule_frame.winfo_children():
                if isinstance(child, RoutineScheduleRow):
                    if freq_selected == "daily":
                        pass
                    # TODO

        # Perform validation
        if not is_valid_description(description):
            messagebox.showerror("Error", "Invalid description.")
            return
        elif type_selected == "goal":
            if not is_valid_date(start_date):
                messagebox.showerror("Error", "Invalid start date.")
                return
            elif not is_valid_date(deadline):
                messagebox.showerror("Error", "Invalid deadline.")
                return
            elif not is_valid_gschedule(gschedule):
                messagebox.showerror("Error", "Invalid goal schedule.")
                return
            elif (
                not goal_attribute_values_compatible(gschedule, start_date, deadline)
                and start_date >= date.today()
            ):
                messagebox.showerror("Error", "Incompatible values.")
                return
        elif type_selected == "routine":
            if not is_valid_rschedule(rschedule):
                messagebox.showerror("Error", "Invalid routine schedule.")
                return

        # Add item to data
        item = {
            "description": description,
            "type": type_selected,
            "active": active,
        }
        if type_selected == "goal":
            item["start_date"] = start_date
            item["deadline"] = deadline
            item["gschedule"] = gschedule
        elif type_selected == "routine":
            item["rschedule"] = rschedule
            item["frequency"] = freq_selected
        add_item(data, item)

        # Return to main screen
        self.master.show_main_screen()


class GoalScheduleRow(ttk.Frame):
    def __init__(self, parent, start_date_picker, deadline_picker, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.start_date_picker = start_date_picker
        self.deadline_picker = deadline_picker
        self.date_picker = DateEntry(self)
        self.date_picker.pack(side=tk.LEFT, padx=5)
        self.duration_entry = ttk.Entry(self, width=5)
        self.duration_entry.pack(side=tk.LEFT, padx=5)
        self.add_button = ttk.Button(self, text="Add", command=self.add_row)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_row)
        self.remove_button.pack_forget()

    def add_row(self):
        if self.is_valid():
            # Disable current row's widgets
            self.date_picker.configure(state="disabled")
            self.duration_entry.configure(state="disabled")

            # Hide "Add" and show "Remove" button for the current row
            self.add_button.pack_forget()
            self.remove_button.pack(side=tk.LEFT, padx=5)

            # Create a new row (active row)
            new_row = GoalScheduleRow(
                self.parent, self.start_date_picker, self.deadline_picker
            )
            new_row.pack(fill=tk.X, padx=5, pady=2)

    def remove_row(self):
        self.destroy()

    def is_valid(self):
        # Get values from widgets
        date_value = self.date_picker.get_date()
        duration_value = self.duration_entry.get()

        # Ensure date is between start date and deadline, and not before today
        if not (
            date_value >= self.start_date_picker.get_date()
            and date_value <= self.deadline_picker.get_date()
            and date_value >= date.today()
        ):
            messagebox.showerror(
                "Invalid Date",
                "The date should be between the start date and deadline, and not before today.",
            )
            return False

        # Check duration validity
        if not is_valid_duration_string(duration_value):
            messagebox.showerror("Invalid Duration", "Please enter a valid duration.")
            return False

        return True


class RoutineScheduleRow(ttk.Frame):
    def __init__(self, parent, routine_var, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.routine_var = routine_var
        self.weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        self.weekday_var = tk.StringVar()
        self.weekday_dropdown = ttk.Combobox(
            self, textvariable=self.weekday_var, values=self.weekdays, state="readonly"
        )
        self.day_entry = ttk.Entry(self, width=5)
        self.yearly_date_picker = DateEntry(self, year=2099)
        self.duration_entry = ttk.Entry(self, width=5)
        self.add_button = ttk.Button(self, text="Add", command=self.add_row)
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_row)
        self.remove_button.pack_forget()
        self.construct_interface()

    def construct_interface(self):
        routine_type = self.routine_var.get()

        # First, clear previous widgets
        for widget in self.winfo_children():
            widget.pack_forget()

        if routine_type == "daily":
            self.duration_entry.pack(side=tk.LEFT, padx=5)
        elif routine_type == "weekly":
            self.weekday_dropdown.pack(side=tk.LEFT, padx=5)
            self.duration_entry.pack(side=tk.LEFT, padx=5)
        elif routine_type == "monthly":
            self.day_entry.pack(side=tk.LEFT, padx=5)
            self.duration_entry.pack(side=tk.LEFT, padx=5)
        elif routine_type == "yearly":
            self.yearly_date_picker.pack(side=tk.LEFT, padx=5)
            self.duration_entry.pack(side=tk.LEFT, padx=5)

        self.add_button.pack(side=tk.LEFT, padx=5)
        # Note: The remove button will only be shown for subsequent rows, not the initial row

    def add_row(self):
        if self.is_valid():
            self.duration_entry.configure(state="disabled")
            if self.routine_var.get() == "weekly":
                self.weekday_dropdown.configure(state="disabled")
            elif self.routine_var.get() == "monthly":
                self.day_entry.configure(state="disabled")
            elif self.routine_var.get() == "yearly":
                self.yearly_date_picker.configure(state="disabled")

            self.add_button.pack_forget()
            self.remove_button.pack(side=tk.LEFT, padx=5)

            new_row = RoutineScheduleRow(self.parent, self.routine_var)
            new_row.pack(fill=tk.X, padx=5, pady=2)

    def remove_row(self):
        self.destroy()

    def is_valid(self):
        routine_type = self.routine_var.get()

        # Check duration validity
        duration_value = self.duration_entry.get()
        if not is_valid_duration_string(duration_value):
            messagebox.showerror("Invalid Duration", "Please enter a valid duration.")
            return False

        # Check day validity
        if routine_type == "weekly":
            weekday_value = self.weekday_var.get()
            if weekday_value not in self.weekdays:
                messagebox.showerror(
                    "Invalid Weekday", "Please select a valid weekday."
                )
                return False
        elif routine_type == "monthly":
            day_value = self.day_entry.get()
            if not is_valid_month_day_str(day_value):
                messagebox.showerror(
                    "Invalid Day", "Please enter a day of month in interval [0, 28)."
                )
                return False

        return True


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen = MainScreen(self)
        self.items_screen = ItemsScreen(self)
        self.delete_screen = DeleteScreen(self)
        self.add_screen = AddScreen(self)
        self.current_screen = None
        self.show_main_screen()

    def show_main_screen(self):
        self.main_screen.refresh_day_view()
        self._show_screen(self.main_screen)

    def show_items_screen(self):
        self.items_screen.refresh_items()
        self._show_screen(self.items_screen)

    def show_delete_screen(self):
        self.delete_screen.refresh_items()
        self._show_screen(self.delete_screen)

    def show_add_screen(self):
        self._show_screen(self.add_screen)

    def _show_screen(self, screen):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.current_screen = screen
        self.current_screen.pack()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save data and quit?"):
            save_data(data)
            self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.geometry("800x600")
    app.mainloop()
