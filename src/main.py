from dataclasses import fields
from functools import partial
from copy import copy

from const import TITLE
from tk_table import table

import spotipy
import tkinter
from tkinter import ttk
import json
from spotipy.oauth2 import SpotifyClientCredentials

config_file = open("config.json")
config_data = json.load(config_file)

window = tkinter.Tk()
page = tkinter.IntVar()
page.set(0)

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=config_data["client_id"], client_secret=config_data["client_secret"]
    )
)

RESULTS_TEMPLATE = [
    ("artist(s)", "song name", "duration", "tempo", "key"),
]


# Tkinter Setup
window.title(TITLE)
window.geometry("720x480")
TABLE_WIDTH = (20, 50, 8, 8, 8)

# Results
results_frame = tkinter.Frame(window)
results_table_data = copy(RESULTS_TEMPLATE)
results_table = table(results_frame, results_table_data, TABLE_WIDTH)

results_data = None


def open_progress_bar():
    progress = ttk.Progressbar(
        window, orient=tkinter.HORIZONTAL, length=100, mode="determinate"
    )
    progress.pack()

    return progress


def search(playlist_id):
    global results_table
    global results_data

    playlist_id = playlist_id()

    results_data = sp.playlist_items(playlist_id=playlist_id)["items"]
    offset = 100
    running = True
    while running:
        more_data = sp.playlist_items(playlist_id=playlist_id, offset=offset + 1)[
            "items"
        ]
        results_data.extend(more_data)
        offset += 100

        if len(more_data) == 0:
            running = False

    display_page(page.get())


def display_page(page_value):
    global results_table
    global results_table_data

    window.title(f"{TITLE} (working... do not close)")
    results_table_data = copy(RESULTS_TEMPLATE)
    results_frame.pack_forget()
    start_val = config_data["search_limit"] * page_value
    for idx, track in enumerate(results_data[start_val:], start=start_val):
        track = track["track"]
        window.title(f"{TITLE} - working song #{idx} | {track['name']}")
        audio_analysis = sp.audio_analysis(track["id"])
        result = (
            track["artists"][0]["name"],
            track["name"],
            f"{int(track['duration_ms'] / (60 * 1000))} min",
            audio_analysis["track"]["tempo"],
            audio_analysis["track"]["key"],
        )
        results_table_data.append(result)

        if idx == config_data["search_limit"] * (page_value + 1):
            break

    results_table = table(results_frame, results_table_data, TABLE_WIDTH)
    results_frame.pack()
    window.title(TITLE)


# Grab
grab_frame = tkinter.Frame(window, width=100)
grab_frame.pack()

playlist_id_label = tkinter.Label(grab_frame, text="playlist id: ")
playlist_id_label.pack(side=tkinter.LEFT)

playlist_id_field = tkinter.Entry(grab_frame, width=60)
playlist_id_field.pack(side=tkinter.LEFT)

search_func_args = partial(search, playlist_id_field.get)
grab_button = tkinter.Button(grab_frame, text="Grab", command=search_func_args)
grab_button.pack(side=tkinter.RIGHT)

# Page Management
page_manage_frame = tkinter.Frame(window, width=100, pady=5)
page_manage_frame.pack()


def advance_page():
    global page
    page.set(page.get() + 1)
    display_page(page.get())


def go_back_page():
    global page
    if page.get() > 0:
        page.set(page.get() - 1)
        display_page(page.get())


prev_page_button = tkinter.Button(
    page_manage_frame, text="Prev Page", command=go_back_page
)
prev_page_button.pack(side=tkinter.LEFT)
next_page_button = tkinter.Button(
    page_manage_frame, text="Next Page", command=advance_page
)
next_page_button.pack(side=tkinter.RIGHT)
page_indicator_label = tkinter.Label(page_manage_frame, textvariable=page)
page_indicator_label.pack(side=tkinter.BOTTOM)

# Show table
results_frame.pack()


# Loop
window.mainloop()
