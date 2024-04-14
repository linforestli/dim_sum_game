import tkinter as tk
from tkinter import messagebox
import serial  # install pyserial to make it work
import threading
import queue

# Set up the port. Change it accordingly to match with your system.
ser = serial.Serial('/dev/cu.usbmodem2101', 9600, timeout=1)

card_icons = {
    "bambooshoot": "bambooshoot.png",
    "shrimp": "shrimp.png",
    "steam": "steam.png",
}

scanned_cards = []
scan_popup = None
data_queue = queue.Queue()


def listen_for_card_scans():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_queue.put(line)


def check_queue():
    try:
        card_data = data_queue.get(block=False)
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
    if len(scanned_cards) == 3 and scan_popup:
        show_combine_button()

def update_popup_with_scan(card_data):
    if card_data in card_icons:
        icon_path = card_icons[card_data]
        icon = tk.PhotoImage(file=icon_path)
        label = tk.Label(scan_popup, text=card_data, image=icon, compound='left')
        label.image = icon  # Keep a reference!
        label.pack()

def show_combine_button():
    combine_button = tk.Button(scan_popup, text="Cook!", command=check_combination)
    combine_button.pack()

def check_combination():
    if set(scanned_cards) == {"bambooshoot", "shrimp", "steam"}:
        result_label = tk.Label(scan_popup, text="You've made a Har Gow!")
        result_label.pack()
        explore_button = tk.Button(scan_popup, text="Explore More", command=show_dish_story)
        explore_button.pack()
    else:
        messagebox.showinfo("Result", "This combination doesn't work.")
    scanned_cards.clear()  # Reset for the next game

def start_game():
    global scanned_cards, scan_popup
    scanned_cards.clear()  # Reset scanned cards
    scan_popup = tk.Toplevel(window)
    scan_popup.title("Scan Cards")
    scan_popup.geometry("600x500")
    tk.Label(scan_popup, text="Add your ingredients!").pack()


def show_dish_story():
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
window.geometry("300x100")

# Start game button
start_button = tk.Button(window, text="Start Game", command=start_game)
start_button.pack(pady=20)

# Start listening for card scans in a separate thread
thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()

window.after(100, check_queue)  # Start checking the queue

window.mainloop()