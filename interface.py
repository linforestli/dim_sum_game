import tkinter as tk
from tkinter import messagebox
import serial # install pyserial to make it work
import threading

# Set up the port. Change it accordingly to match with your system.
ser = serial.Serial('/dev/cu.usbmodem2101', 9600, timeout=1)


def listen_for_card_scans():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line == "Added Tapioca Starch!":
                window.event_generate('<<Card1Scanned>>', when='tail')


def on_card1_scanned(event):
    messagebox.showinfo("Dim Sum Game", "Added Tapioca Starch!")


window = tk.Tk()
window.title("Dim Sum Game")
window.geometry("300x100")

window.bind('<<Card1Scanned>>', on_card1_scanned)

thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()

window.mainloop()
