import tkinter as tk
from tkinter import messagebox
from tkinter import *
#import serial  # install pyserial to make it work
import threading
import queue
import csv
import json

# Set up the port
#ser = serial.Serial('/dev/cu.usbmodem2101', 9600, timeout=1)

card_icons = {
    "bambooshoot": "bambooshoot.png",
    "shrimp": "final cards/shrimp.png",
    "steam": "steam.png",
}

ingredient_map = {}
icon_map = {}
with open('data/encoded-rfid_cards.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    ingredient_map = {rows[0]: rows[1] for rows in reader}

with open('data/icon_path.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    icon_map = {rows[0]: rows[1] for rows in reader}

with open('data/combinations.json', 'r') as json_file:
    combinations = json.load(json_file)

scanned_cards = []
scan_popup = None
data_queue = queue.Queue()

# Set up GUI
background_color = "#FBFAED"

def open_instructions():
    main_screen.pack_forget()
    instructions_frame.pack()

def open_main():
    instructions_frame.pack_forget()
    story_frame.pack_forget()
    scan_cards_frame.pack_forget()
    results_frame.pack_forget()
    main_screen.pack()

def open_story():
    main_screen.pack_forget()
    story_frame.pack()

def back_to_home_confirm():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to go back to home?")
    if result == 'yes':
        scan_cards_frame.pack_forget()
        open_main()

# Set up functions for game mechanism

#def listen_for_card_scans():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_queue.put(line)


def check_queue():
    try:
        card_uid = data_queue.get(block=False)
        card_data = ingredient_map.get(card_uid.upper(), None)
        on_card_scanned(card_data)
    except queue.Empty:
        pass
    window.after(100, check_queue)


def on_card_scanned(card_data):
    if card_data in scanned_cards:  # Prevent duplicate scans
        messagebox.showwarning("Warning", "Card already scanned!")
        return
    scanned_cards.append(card_data)
    if scan_card_frame: # TODO: cannot call out frame here, should be a variable
        update_frame_with_scan(card_data)
        if len(scanned_cards) >= 4 and scan_card_frame:  # Changed to >= to match new logic
            show_combine_button()


def update_frame_with_scan(card_data):
    if card_data in icon_map:
        icon_path = icon_map[card_data]
        icon = tk.PhotoImage(file=icon_path)
        label = tk.Label(scan_card_frame, text=card_data, image=icon, compound='left')
        label.image = icon  # Keep a reference!
        label.pack()


def show_combine_button():
    combine_button = tk.Button(scan_card_frame, text="Cook!", command=check_combination)
    combine_button.pack()


def check_combination():
    global scanned_cards
    total_scanned = len(scanned_cards)

    if total_scanned < 3:
        return
    elif total_scanned > 4:
        print("Too many cards scanned, resetting...")
        messagebox.showinfo("Info", "Too many cards scanned, resetting...")
        scanned_cards.clear()
        return

    scanned_set = set(scanned_cards)
    found_valid_combination = False

    for dish, ingredients in combinations.items():
        ingredient_set = set(ingredients)
        print(ingredient_set)
        if ingredient_set == scanned_set:
            # TODO: if this condition is met, should it trigger the show_combine_button() or show_results()
            scanned_cards.clear()
            found_valid_combination = True
            break  # Exit the loop after finding a valid combination

    if not found_valid_combination and total_scanned == 4:
        # TODO: in case failed
        messagebox.showinfo("Result", "This combination doesn't work.")
        scanned_cards.clear()

def start_scan():
    global scanned_cards, scan_popup
    scanned_cards.clear()  # Reset scanned cards
    box1 = tk.Frame(scan_cards_frame, height=50, width=50, background=background_color)
    box1.pack(side=LEFT, padx=5, pady=5)

    # TODO: test with 1 card first if it shows up
    box1_image = tk.PhotoImage(file="final cards/beef.png") # TODO: Trigger this by setting a variable for file name (which search for items in the database, then call it here)
    box1_image_label = tk.Label(wrapper_box, image=wrapper_image, background=background_color)
    box1_image_label.pack()


def show_results():
    scan_cards_frame.pack_forget()
    results_frame.pack()
    # TODO: Trigger this by setting a variable for dish_story (same as file name)
    dish_story = """The har gow dumpling originated in a teahouse in the Wucu village, 
       a suburban region of Guangzhou. It appeared on the outskirts at a teahouse in the Wucu village; 
       the owner was said to have had access to a river right outside, where shrimp would be caught and directly made into the fresh stuffing for har gow dumplings. """

    story_label = tk.Label(scan_popup, text=dish_story, wraplength=250)
    story_label.pack()

    close_button = tk.Button(scan_popup, text="Close", command=scan_popup.destroy)
    close_button.pack()


window = tk.Tk()
window.title("Dim Sum Game")
window.geometry("1500x800")

# Main screen 
main_screen = tk.Frame(window, bg="#FBFAED")
main_screen.pack(padx=20, pady=20)

title_image = tk.PhotoImage(file="final cards/header.png")
title_label = tk.Label(main_screen, image=title_image, background=background_color)
title_label.pack(pady=10)

start_button = tk.Button(main_screen, text="Play", command=open_story, borderwidth=None).pack(side=LEFT, pady=20)
instructions_button = tk.Button(main_screen, text="Instructions", command=open_instructions).pack(side=LEFT, pady=20)


# Instructions Screen
instructions_frame = tk.Frame(window, background=background_color)
instructions_frame.pack(expand=TRUE, pady=10)
instructions_label = tk.Label(instructions_frame, text="Instructions", font=("Roboto", "32"))
instructions_label.pack(expand=TRUE, pady=10)

instructions_text = """
Welcome to the Dim Sum Game!

How to play:
1. Choose your wrapper, vegetables, or protein of your choice, and a cooking method 
2. Tap each of the card on the reader 
3. Wait for the machine to respond 
4. Tadaa! You have made a dish. 
"""

instructions_text_label = tk.Label(instructions_frame, text=instructions_text, background=background_color, font=("Roboto", "24"), justify=LEFT).pack(pady=10)
back_button = tk.Button(instructions_frame, background=background_color, text="Back", command=open_main, borderwidth=0).pack(pady=10)

# Story screen
story_frame = tk.Frame(window, background=background_color)
story_frame.pack(pady=10)

story_text = """
Once upon a time, in a bustling city filled with the aroma of delicious food, there was a quaint little dim sum restaurant called "Dim Sum Delights." The restaurant was known far and wide for its exquisite dim sum dishes, each bursting with flavor and creativity. 

One day, you decided to visit Dim Sum Delights for a fun lunch outing. As you sat down at their table, they noticed a unique set of cards placed in front of them. The cards were adorned with colorful illustrations of various dim sum ingredients like shrimp, pork, and mushrooms. 

Now, tap your cards to explore the world of dim sum... 
"""
story_text_label = tk.Label(story_frame, text=story_text, wraplength=1000, background=background_color, font=("Roboto", "24"), justify=LEFT).pack(pady=10)
continue_button = tk.Button(story_frame, text="Continue", command=check_combination).pack(pady=10)

# Initiate scan cards frame
scan_cards_frame = tk.Frame(window, background=background_color)
scan_cards_frame.pack(padx=10, pady=10)
scan_cards_label = tk.Label(scan_cards_frame, text="Tap to scan", wraplength=250, font=("Roboto", "24"), background=background_color).pack(pady=10)
# TODO: Add a function to initiate cards popping up when scanned


# Initiate results frame
results_frame = tk.Frame(window, background=background_color)
results_label = tk.Label(results_frame, text="Tadaa!", font=("Roboto", 32))
results_frame.pack(pady=10)


# TODO: Update results test by search and replace in the database
            results_text = """
            You've made [dish name]!

            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis auctor elit sed vulputate mi sit amet. Sem integer vitae justo eget magna. Vestibulum morbi blandit cursus risus at ultrices. Scelerisque eu ultrices vitae auctor eu augue. Laoreet suspendisse interdum consectetur libero id faucibus nisl tincidunt eget. Lacinia quis vel eros donec ac odio tempor orci. Nec dui nunc mattis enim ut tellus. Imperdiet dui accumsan sit amet nulla. At tellus at urna condimentum mattis pellentesque id nibh. Diam vel quam elementum pulvinar etiam non quam lacus suspendisse. Cursus vitae congue mauris rhoncus aenean vel elit. Id cursus metus aliquam eleifend mi in nulla posuere sollicitudin. Fringilla est ullamcorper eget nulla facilisi etiam dignissim. Dapibus ultrices in iaculis nunc sed augue lacus. Vehicula ipsum a arcu cursus vitae congue. Nisi est sit amet facilisis. Ac tincidunt vitae semper quis lectus nulla at. Fusce ut placerat orci nulla pellentesque dignissim enim sit amet.
            """

            results_text_label = tk.Label(results_frame, text=results_text, wraplength=1000, background=background_color, font=("Roboto", "16")).pack(pady=10)

            results_image = tk.PhotoImage(file="final cards/hargow.png")
            results_image_label = tk.Label(results_frame, image=results_image)
            results_image_label.pack()

            continue_button = tk.Button(results_frame, text="Continue", command=scan_cards).pack(pady=10)
            back_button = tk.Button(results_frame, text="Back", command=back_to_home_confirm).pack(pady=10)
# Start listening for card scans in a separate thread
#thread = threading.Thread(target=listen_for_card_scans, daemon=True)
#thread.start()

#window.after(100, check_queue)  # Start checking the queue

open_main()
window.mainloop()

