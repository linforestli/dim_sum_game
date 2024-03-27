import tkinter as tk
from tkinter import messagebox
from tkinter import *
import serial  # install pyserial to make it work
import threading
import queue
import csv
import json

# Set up the port
ser = serial.Serial('/dev/cu.usbmodem2101', 9600, timeout=1)

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

# Set up functions for game mechanism

def listen_for_card_scans():
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
    if scan_card_frame:
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
            # TODO: you can choose to initialize your result frame here
            messagebox.showinfo("Success", f"You've made a {dish}!")
            scanned_cards.clear()
            found_valid_combination = True
            break  # Exit the loop after finding a valid combination

    if not found_valid_combination and total_scanned == 4:
        # TODO: in case failed
        messagebox.showinfo("Result", "This combination doesn't work.")
        scanned_cards.clear()

# TODO: update the scan card frame initialization
def start_scan():
    global scanned_cards, scan_popup
    scanned_cards.clear()  # Reset scanned cards
    scan_popup = tk.Toplevel(window)
    scan_popup.title("Scan Cards")
    scan_popup.geometry("1500x800")
    tk.Label(scan_popup, text="Add your ingredients!").pack()


def show_dish_story():
    # Your existing show_dish_story function here
    # Assuming you want to replace the current popup content with the story
    for widget in scan_popup.winfo_children():
        widget.destroy()  # Clear the current content of the popup

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

start_button = tk.Button(main_screen, text="Play", command=open_story, image=resized_start_btn, borderwidth=None).pack(side=LEFT, pady=20)
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
back_button = tk.Button(instructions_frame, background=background_color, image=resized_back_btn , text="Back", command=open_main, borderwidth=0).pack(pady=10)


# Start listening for card scans in a separate thread
thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()

window.after(100, check_queue)  # Start checking the queue

window.mainloop()
