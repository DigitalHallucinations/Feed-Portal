# modules/settings/settings.py

import tkinter as tk
from tkinter import ttk
import configparser
from modules.tooltip import ToolTip
from modules.logging.logger import setup_logger

logger = setup_logger('settings')

def load_settings(self):
    """Loads settings from the config.ini file."""
    logger.info("Loading settings from config.ini...")
    config = configparser.ConfigParser()
    config.read("config.ini")

    self.entries_per_feed = config.getint("FeedSettings", "entries_per_feed", fallback=10)
    self.refresh_interval_mins = config.getint("FeedSettings", "refresh_interval_mins", fallback=30)
    self.display_format = config.get("FeedSettings", "display_format", fallback="Simple List")

def open_settings(self):
    """Opens a new window for adjusting settings."""
    logger.info("Opening settings window...")
    settings_window = tk.Toplevel(self.master)
    settings_window.title("Settings")
    settings_window.configure(bg=self.window_bg)
    settings_window_width = int(400 * self.scale_factor)
    settings_window_height = int(200 * self.scale_factor)
    settings_window.geometry(f"{settings_window_width}x{settings_window_height}")

    font_style = (self.font_family, int(self.font_size * 10 * self.scale_factor))

    style = ttk.Style()
    style.configure("Settings.TLabel", background=self.window_bg, foreground=self.font_color, font=font_style)

    entries_label = ttk.Label(settings_window, text="Entries per Feed:", style="Settings.TLabel")
    entries_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entries_var = tk.IntVar(value=self.entries_per_feed)
    entries_spinbox = tk.Spinbox(settings_window, from_=1, to=100, textvariable=entries_var, bg=self.spinbox_bg, fg=self.font_color, font=font_style)        
    entries_spinbox.grid(row=0, column=1, padx=5, pady=5)
    ToolTip(entries_spinbox, "Set the number of entries per feed", font_style) 

    refresh_label = ttk.Label(settings_window, text="Refresh Interval (mins):", style="Settings.TLabel")
    refresh_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    refresh_var = tk.IntVar(value=self.refresh_interval_mins)
    refresh_spinbox = tk.Spinbox(settings_window, from_=1, to=1440, textvariable=refresh_var, bg=self.spinbox_bg, fg=self.font_color, font=font_style)        
    refresh_spinbox.grid(row=1, column=1, padx=5, pady=5)
    ToolTip(refresh_spinbox, "Set the refresh interval in minutes", font_style) 

    format_label = ttk.Label(settings_window, text="Display Format:", style="Settings.TLabel")
    format_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    format_var = tk.StringVar(value=self.display_format)
    format_options = ["Simple List", "Detailed List", "Card View"]
    format_dropdown = tk.OptionMenu(settings_window, format_var, self.display_format, *format_options)
    format_dropdown.configure(bg=self.button_bg, fg=self.font_color, font=font_style)
    format_dropdown.grid(row=2, column=1, padx=5, pady=5)
    ToolTip(format_dropdown, "Select the display format for entries", font_style) 

    save_button = tk.Button(settings_window, text="Save", command=lambda: save_settings(self, entries_var.get(), refresh_var.get(), format_var.get()), bg=self.button_bg, fg=self.font_color, font=font_style)        
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    ToolTip(save_button, "Save the settings", font_style) 

def save_settings(self, entries_per_feed, refresh_interval_mins, display_format):
    """Saves the current settings to the config.ini file."""
    logger.info("Saving settings to config.ini...")
    config = configparser.ConfigParser()
    config.read("config.ini")

    if not config.has_section("FeedSettings"):
        config.add_section("FeedSettings")

    config.set("FeedSettings", "entries_per_feed", str(entries_per_feed))
    config.set("FeedSettings", "refresh_interval_mins", str(refresh_interval_mins))
    config.set("FeedSettings", "display_format", display_format)

    with open("config.ini", "w") as configfile:
        config.write(configfile)

    self.entries_per_feed = entries_per_feed
    self.refresh_interval_mins = refresh_interval_mins
    self.display_format = display_format

    self.refresh_feeds() 