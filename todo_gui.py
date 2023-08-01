from todo import data
from helpers import *
import tkinter as tk
from datetime import date


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
        self.add_button = tk.Button(self.menu, text=f"Add Item")
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
        self.today_label = tk.Label(self.day_view, text=str(date.today()))
        self.today_label.pack(pady=5, padx=10)

        self.item_list = get_items_for_date(data, date.today())
        for item in self.item_list:
            self.item_label = tk.Label(self.day_view, text=item["description"])
            self.item_label.pack(pady=5, padx=10)


class ItemsScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="All items")
        self.label.pack()

        for item in data["items"]:
            self.item_label = tk.Label(self, text=item["description"])
            self.item_label.pack(padx=10, pady=5)

        self.button = tk.Button(
            self, text="Go to Main Screen", command=self.master.show_main_screen
        )
        self.button.pack()


class DeleteScreen(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="Select item to delete.")
        self.label.pack()

        self.v = tk.IntVar()
        for i, item in enumerate(data["items"]):
            self.item_button = tk.Radiobutton(
                self,
                text=item["description"],
                variable=self.v,
                value=i,
            )
            self.item_button.pack(padx=10, pady=5)

        self.select_button = tk.Button(
            self, text="Select", command=lambda: print(self.v.get())
        )
        self.select_button.pack()

        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.master.show_main_screen
        )
        self.cancel_button.pack()


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen = MainScreen(self)
        self.items_screen = ItemsScreen(self)
        self.delete_screen = DeleteScreen(self)
        self.current_screen = None
        self.show_main_screen()

    def show_main_screen(self):
        self._show_screen(self.main_screen)

    def show_items_screen(self):
        self._show_screen(self.items_screen)

    def show_delete_screen(self):
        self._show_screen(self.delete_screen)

    def _show_screen(self, screen):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.current_screen = screen
        self.current_screen.pack()


if __name__ == "__main__":
    app = MainApplication()
    app.geometry("600x400")
    app.mainloop()
