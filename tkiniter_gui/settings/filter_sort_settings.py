# modules/settings/filter_sort_settings.py

import tkinter as tk
from tkinter import ttk
import json
from tkcalendar import Calendar 
from datetime import datetime
from modules.tooltip import ToolTip
from modules.logging.logger import setup_logger

logger = setup_logger('filter_sorta_settings')

def load_filter_sort_settings(self):
    try:
        with open("filters.json", "r") as f:
            self.filters = json.load(f)
        with open("sorting.json", "r") as f:
            self.sorting = json.load(f)

        if self.filters["date_range"]["start"]:
            self.filters["date_range"]["start"] = datetime.strptime(self.filters["date_range"]["start"], '%Y-%m-%d')
        else:
            self.filters["date_range"]["start"] = None

        if self.filters["date_range"]["end"]:
            self.filters["date_range"]["end"] = datetime.strptime(self.filters["date_range"]["end"], '%Y-%m-%d')
        else:
            self.filters["date_range"]["end"] = None

    except FileNotFoundError:
        self.filters = {
            "keywords": [],
            "date_range": {
                "start": None,
                "end": None
            },
            "categories": []
        }
        self.sorting = {
            "method": "date",
            "order": "descending"
        }

def open_filter_settings(self):
    filter_settings_window = tk.Toplevel(self.master)
    filter_settings_window.title("Filter Settings")
    filter_settings_window.configure(bg=self.window_bg)  
    
    setup_filter_settings_ui(self, filter_settings_window, self.font_family, self.font_size, self.font_color, self.window_bg, self.spinbox_bg, self.button_bg)

def setup_filter_settings_ui(self, window, font_family, font_size, font_color, window_bg, spinbox_bg, button_bg):
    font_style = (font_family, int(font_size * 10 * self.scale_factor))

    keyword_label = ttk.Label(window, text="Keywords:", font=font_style, background=window_bg, foreground=font_color)
    keyword_label.grid(row=0, column=0, padx=5, pady=5)

    self.keyword_entry = tk.Entry(window, width=40, bg=spinbox_bg, fg=font_color, font=font_style)
    self.keyword_entry.grid(row=0, column=1, padx=5, pady=5)

    date_range_label = ttk.Label(window, text="Date Range:", font=font_style, background=window_bg, foreground=font_color)
    date_range_label.grid(row=1, column=0, padx=5, pady=5)

    date_frame = tk.Frame(window, bg=window_bg)
    date_frame.grid(row=1, column=1, padx=5, pady=5)

    self.start_date_calendar = Calendar(date_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    self.start_date_calendar.pack(side=tk.LEFT)

    self.end_date_calendar = Calendar(date_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    self.end_date_calendar.pack(side=tk.LEFT)

    category_label = ttk.Label(window, text="Categories:", font=font_style, background=window_bg, foreground=font_color)
    category_label.grid(row=2, column=0, padx=5, pady=5)

    category_frame = tk.Frame(window, bg=window_bg)
    category_frame.grid(row=2, column=1, padx=5, pady=5)

    self.category_listbox = tk.Listbox(category_frame, selectmode=tk.MULTIPLE, bg=spinbox_bg, fg=font_color, font=font_style)
    self.category_listbox.pack(side=tk.LEFT)

    categories = self.rss_feed_reader.get_categories()
    for category in categories:
        self.category_listbox.insert(tk.END, category)

    sort_label = ttk.Label(window, text="Sort By:", font=font_style, background=window_bg, foreground=font_color)
    sort_label.grid(row=3, column=0, padx=5, pady=5)

    sort_frame = tk.Frame(window, bg=window_bg)
    sort_frame.grid(row=3, column=1, padx=5, pady=5)

    self.sort_var = tk.StringVar(value=self.sorting["method"])
    sort_options = ["Date", "Title"]
    sort_dropdown = tk.OptionMenu(sort_frame, self.sort_var, *sort_options)
    sort_dropdown.configure(bg=spinbox_bg, fg=font_color, font=font_style)
    sort_dropdown.pack(side=tk.LEFT)

    order_label = ttk.Label(window, text="Sort Order:", font=font_style, background=window_bg, foreground=font_color)
    order_label.grid(row=4, column=0, padx=5, pady=5)

    order_frame = tk.Frame(window, bg=window_bg)
    order_frame.grid(row=4, column=1, padx=5, pady=5)

    self.order_var = tk.StringVar(value=self.sorting["order"])
    order_options = ["Ascending", "Descending"]
    order_dropdown = tk.OptionMenu(order_frame, self.order_var, *order_options)
    order_dropdown.configure(bg=spinbox_bg, fg=font_color, font=font_style)
    order_dropdown.pack(side=tk.LEFT)

    save_button = tk.Button(window, text="Save", command=lambda: save_filter_sort_settings(self), bg=button_bg, fg=font_color, font=font_style)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

def save_filter_sort_settings(self):
    keywords = self.keyword_entry.get().strip().split(",")

    start_date_str = self.start_date_calendar.get_date()
    end_date_str = self.end_date_calendar.get_date()

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    except ValueError:
        start_date = None

    try:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        end_date = None

    selected_categories = [self.category_listbox.get(i) for i in self.category_listbox.curselection()]

    self.filters.update({
        "keywords": keywords,
        "date_range": {"start": start_date_str, "end": end_date_str},
        "categories": selected_categories
    })

    with open("filters.json", "w") as f:
        json.dump(self.filters, f, indent=4)

    self.sorting.update({
        "method": self.sort_var.get().lower(),
        "order": self.order_var.get().lower()
    })

    with open("sorting.json", "w") as f:
        json.dump(self.sorting, f, indent=4)

    self.refresh_feeds()