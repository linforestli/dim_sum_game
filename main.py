import tkinter as tk
from tkinter import messagebox
from tkinter import *
import serial  # install pyserial to make it work
import threading
import queue
import csv
import json

# Set up the port
ser = serial.Serial('COM7', 9600, timeout=1)

ingredient_map = {}
icon_map = {}
story_map = {}

with open('data/encoded-rfid_cards.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    ingredient_map = {rows[0]: rows[1] for rows in reader}

with open('data/icon_path.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    icon_map = {rows[0]: rows[1] for rows in reader}

with open('data/combinations.json', 'r') as json_file:
    combinations = json.load(json_file)

with open('data/dish_story.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    story_map = {rows[0]: rows[1] for rows in reader}


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

def open_scan_cards():
    story_frame.pack_forget()
    results_frame.pack_forget()
    scan_cards_frame.pack()

def back_to_home_confirm():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to go back to home?")
    if result == 'yes':
        scan_cards_frame.pack_forget()
        open_main()

# Set up functions for game mechanism

def listen_for_card_scans():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_queue.put(line)


def check_queue():
    global card_data
    try:
        card_uid = data_queue.get(block=False)
        card_data = ingredient_map.get(card_uid.upper(), None)
        on_card_scanned(card_data)
    except queue.Empty:
        pass
    window.after(100, check_queue)

combine_button_shown = False

def on_card_scanned(card_data):
    if card_data in scanned_cards:  # Prevent duplicate scans
        messagebox.showwarning("Warning", "Card already scanned!")
        return
    scanned_cards.append(card_data)
    update_frame_with_scan(card_data)
    if len(scanned_cards) >= 4:
        show_combine_button()

# Update card photo when scanned
def update_frame_with_scan(card_data):
    if card_data in icon_map:
        icon_path = icon_map[card_data]
        icon = tk.PhotoImage(file=icon_path)
        icon_resized = icon.subsample(2, 2)
        label = tk.Label(cards_box, image=icon_resized, background=background_color)
        label.image = icon_resized
        label.pack(side=LEFT)

# Show combine button when all ingredients are scanned
def show_combine_button():
    global combine_button_shown
    if not combine_button_shown:
        combine_button = tk.Button(scan_cards_frame, text="Cook!", command=check_combination)
        combine_button.pack(side=TOP)
        combine_button_shown = True

# Check the combination to show results
def check_combination():
    global scanned_cards
    total_scanned = len(scanned_cards)

    if total_scanned < 3:
        return
    elif total_scanned > 4:
        messagebox.showinfo("Info", "Too many cards scanned, resetting...")
        scanned_cards.clear()
        return

    scanned_set = set(scanned_cards)
    found_valid_combination = False

    for dish, ingredients in combinations.items():
        ingredient_set = set(ingredients)
        if ingredient_set == scanned_set:
            # TODO: here should be the results frame + display the result
            scanned_cards.clear()
            found_valid_combination = True
            show_results(dish)
            break  # Exit the loop after finding a valid combination

    if not found_valid_combination and total_scanned >= 4:
        # TODO: in case failed
        clear_button = tk.Button(scan_cards_frame, background=background_color, text="Clear", command=clear_ingredient,
                                borderwidth=0).pack(pady=10)
        messagebox.showinfo("Result", "This combination doesn't work.")


def clear_ingredient():
    scanned_cards.clear()
    for widget in cards_box.winfo_children():
        widget.destroy()



def start_scan():
    global scanned_cards, scan_popup
    scanned_cards.clear()  # Reset scanned cards
    check_queue()

# Show results
def show_results(dish):
    scan_cards_frame.pack_forget()
    results_frame.pack()
    for food in story_map:
        if food == dish:
            dish_story = story_map[food]
    story_label = tk.Label(results_frame, text=dish_story, wraplength=250)
    story_label.pack()
    
    for food in icon_map:
        if food == dish:
            results_icon = icon_map[food]
    
    results_icon = tk.PhotoImage(file=results_icon)
    results_image = tk.Label(results_frame, image=results_icon, background=background_color)
    results_image.image = results_icon
    results_image.place(relx=0.5, rely=0.6, anchor=CENTER)

    close_button = tk.Button(scan_popup, text="Close", command=scan_popup.destroy)
    close_button.pack()

# Initiate game
window = tk.Tk()
window.configure(bg=background_color)
window.title("Dim Sum Game")
window.geometry("1500x800")

# Main screen 
main_screen = tk.Frame(window, bg=background_color)
main_screen.pack(fill=BOTH, expand=TRUE)

## Background for landing page
landing_bg_img = tk.PhotoImage(file='final cards/landing_background.png')
landing_bg = tk.Label(main_screen, image=landing_bg_img)
landing_bg.pack()

## Game header for landing page
title_image = tk.PhotoImage(file="final cards/header.png")
title_label = tk.Label(main_screen, image=title_image)
title_label.place(relx=0.5, rely=0.3, anchor=CENTER)

## Buttons for main screen
start_btn_img = PhotoImage(file='final cards/start_button.png')
start_button = Button(main_screen, command=open_story, image=start_btn_img, borderwidth=0, background=background_color)
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

instructions_btn_img = PhotoImage(file='final cards/instructions_button.png')
instructions_button = Button(main_screen, command=open_instructions, image=instructions_btn_img, borderwidth=0, background=background_color)
instructions_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Instructions Screen
instructions_frame = tk.Frame(window, background=background_color)
instructions_frame.pack(expand=TRUE, pady=10)
instructions_label = tk.Label(instructions_frame, text="Instructions", font=("Roboto", "32"), background=background_color)
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

back_btn_img = PhotoImage(file='final cards/back_button.png')
back_button = Button(instructions_frame, image= back_btn_img, command=open_main, borderwidth=0)
back_button.pack(anchor=CENTER)

# Story screen
story_frame = tk.Frame(window, background=background_color)
story_frame.pack(pady=10)

story_text = """
Once upon a time, in a bustling city filled with the aroma of delicious food, there was a quaint little dim sum restaurant called "Dim Sum Delights." The restaurant was known far and wide for its exquisite dim sum dishes, each bursting with flavor and creativity. 

One day, you decided to visit Dim Sum Delights for a fun lunch outing. As you sat down at their table, they noticed a unique set of cards placed in front of them. The cards were adorned with colorful illustrations of various dim sum ingredients like shrimp, pork, and mushrooms. 

Now, tap your cards to explore the world of dim sum... 
"""
story_text_label = tk.Label(story_frame, text=story_text, wraplength=1000, background=background_color, font=("Roboto", "24"), justify=LEFT).pack(pady=10)

continue_btn_img = PhotoImage(file='final cards/continue_button.png')
continue_button = tk.Button(story_frame, background=background_color, image=continue_btn_img, command=open_scan_cards, borderwidth=0)
continue_button.pack(anchor=CENTER)

# Initiate scan cards frame
scan_cards_frame = tk.Frame(window, background=background_color)
scan_cards_frame.pack(padx=10, pady=10)
scan_cards_label = tk.Label(scan_cards_frame, text="Tap to scan", wraplength=250, font=("Roboto", "24"), background=background_color).pack(pady=10)

cards_box = tk.Frame(scan_cards_frame)
cards_box.pack(padx=10, pady=10)



# Initiate results frame
results_frame = tk.Frame(window, background=background_color)
results_frame.pack(fill=BOTH, expand=TRUE)

## Background for results page
results_bg_img = tk.PhotoImage(file='final cards/results_background.png')
results_bg = tk.Label(results_frame, image=results_bg_img)
results_bg.pack()

# continue_button = tk.Button(results_frame, text="Continue", command=start_scan).pack(pady=10)
#back_button = tk.Button(results_frame, text="Back", command=back_to_home_confirm).pack(pady=10)

# Start listening for card scans in a separate thread
thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()

window.after(100, check_queue)  # Start checking the queue

open_main()
window.mainloop()

