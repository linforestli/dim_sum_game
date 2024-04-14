import serial  # install pyserial to make it work
import threading
import queue
import csv
import json

# Set up the port. Change it accordingly to match with your system.
ser = serial.Serial('/dev/cu.usbmodem2101', 9600, timeout=1)

ingredient_map = {}
with open('../data/encoded-rfid_cards.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    ingredient_map = {rows[0].upper(): rows[1] for rows in reader}  # Ensure keys are uppercase

# Load combinations from JSON
with open('../data/combinations.json', 'r') as json_file:
    combinations = json.load(json_file)

scanned_cards = []
data_queue = queue.Queue()


def listen_for_card_scans():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_queue.put(line)


def process_card_scans():
    while True:
        try:
            card_uid = data_queue.get(timeout=1)
            card_data = ingredient_map.get(card_uid.upper(), None)
            if card_data:
                if card_data not in scanned_cards:
                    scanned_cards.append(card_data)
                    print(f"Card Scanned: {card_data}")
                    check_combination()
                else:
                    print("Card already scanned.")
        except queue.Empty:
            continue


def check_combination():
    global scanned_cards
    total_scanned = len(scanned_cards)

    if total_scanned < 3:
        return
    elif total_scanned > 4:
        print("Too many cards scanned, resetting...")
        scanned_cards.clear()
        return

    scanned_set = set(scanned_cards)
    found_valid_combination = False

    for dish, ingredients in combinations.items():
        ingredient_set = set(ingredients)
        if ingredient_set <= scanned_set:
            print(f"You've made a {dish}!")
            scanned_cards.clear()
            found_valid_combination = True

    if not found_valid_combination and total_scanned == 4:
        print("This combination doesn't work.")
        scanned_cards.clear()


# thread starts
thread = threading.Thread(target=listen_for_card_scans, daemon=True)
thread.start()
process_card_scans()
