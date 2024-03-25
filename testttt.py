import tkinter as tk
from tkinter import messagebox
import serial  # install pyserial to make it work
import threading
import queue
import csv
import json

# Set up the port. Change it accordingly to match with your system.
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

def open_instructions():
    instruction_window = tk.Toplevel(window)
    instruction_window.title("Instructions")
    instruction_window.geometry("600x400")
    tk.Label(instruction_window, text="Instructions on how to play the game...").pack(pady=20)
    tk.Button(instruction_window, text="Back", command=instruction_window.destroy).pack()

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
        print(card_data)
        on_card_scanned(card_data)
    except queue.Empty:
        pass
    window.after(100, check_queue)


def on_card_scanned(card_data):
    if card_data in scanned_cards:  # Prevent duplicate scans
        messagebox.showwarning("Warning", "Card already scanned!")
        return
    scanned_cards.append(card_data)
    if scan_popup:
        update_popup_with_scan(card_data)
        if len(scanned_cards) >= 4 and scan_popup:  # Changed to >= to match new logic
            show_combine_button()


def update_popup_with_scan(card_data):
    if card_data in icon_map:
        icon_path = icon_map[card_data]
        icon = tk.PhotoImage(file=icon_path)
        label = tk.Label(scan_popup, text=card_data, image=icon, compound='left')
        label.image = icon  # Keep a reference!
        label.pack()


def show_combine_button():
    combine_button = tk.Button(scan_popup, text="Cook!", command=check_combination)
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
            messagebox.showinfo("Success", f"You've made a {dish}!")
            scanned_cards.clear()
            found_valid_combination = True
            break  # Exit the loop after finding a valid combination

    if not found_valid_combination and total_scanned == 4:
        messagebox.showinfo("Result", "This combination doesn't work.")
        scanned_cards.clear()

def start_game():
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

# Start game button
start_button = tk.Button(window, text="Start Game", command=start_game)
start_button.pack(pady=20)

instruction_button = tk.Button(window, text="Instructions", command=open_instructions)
instruction_button.pack(pady=20)

# Start listening for card scans in a separate thread
thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()

window.after(100, check_queue)  # Start checking the queue

window.mainloop()
