import tkinter as tk
from tkinter import *
from tkinter import messagebox

background_color = "#FBFAED"

window = tk.Tk()
window.configure(bg=background_color)
window.title("Dim Sum Game")
window.geometry("1500x800")

back_btn= PhotoImage(file='final cards/back_button.png')
resized_back_btn = back_btn.subsample(2, 2)

start_btn = PhotoImage(file='final cards/start_button.png')
resized_start_btn = start_btn.subsample(2,2)

def start_game():
    main_screen.pack()

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

def scan_cards():
    story_frame.pack_forget()
    results_frame.pack_forget()
    scan_cards_frame.pack()

def open_results():
    scan_cards_frame.pack_forget()
    results_frame.pack()
    
def back_to_home_confirm():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to go back to home?")
    if result == 'yes':
        scan_cards_frame.pack_forget()
        open_main()

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

# Story screen
story_frame = tk.Frame(window, background=background_color)
story_frame.pack(pady=10)

story_text = """
Once upon a time, in a bustling city filled with the aroma of delicious food, there was a quaint little dim sum restaurant called "Dim Sum Delights." The restaurant was known far and wide for its exquisite dim sum dishes, each bursting with flavor and creativity. 

One day, you decided to visit Dim Sum Delights for a fun lunch outing. As you sat down at their table, they noticed a unique set of cards placed in front of them. The cards were adorned with colorful illustrations of various dim sum ingredients like shrimp, pork, and mushrooms. 

Now, tap your cards to explore the world of dim sum... 
"""
story_text_label = tk.Label(story_frame, text=story_text, wraplength=1000, background=background_color, font=("Roboto", "24"), justify=LEFT).pack(pady=10)
continue_button = tk.Button(story_frame, text="Continue", command=scan_cards).pack(pady=10)

# Scan card screen
scan_cards_frame = tk.Frame(window, background=background_color)
scan_cards_frame.pack(padx=10, pady=10)

scan_cards_label = tk.Label(scan_cards_frame, text="Tap to scan", wraplength=250, font=("Roboto", "24"), background=background_color).pack(pady=10)

# Wrapper box
wrapper_box = tk.Frame(scan_cards_frame, height=50, width=50, background=background_color)
wrapper_box.pack(side=LEFT, padx=5, pady=5)

wrapper_box_label = tk.Label(wrapper_box, text="Choose your wrapping", background=background_color)
wrapper_box_label.pack(pady=10)

wrapper_image = tk.PhotoImage(file="final cards/beef.png")
wrapper_image_label = tk.Label(wrapper_box, image=wrapper_image, background=background_color)
wrapper_image_label.pack()

# Protein box
protein_box = tk.Frame(scan_cards_frame, height=50, width=50, background=background_color)
protein_box.pack(side=LEFT)

protein_box_label = tk.Label(protein_box, text="Choose your protein", background=background_color)
protein_box_label.pack(pady=10)

protein_image = tk.PhotoImage(file="final cards/beef.png")
protein_image_label = tk.Label(protein_box, image=protein_image, background=background_color)
protein_image_label.pack()

# Vegetables box
vegetable_box = tk.Frame(scan_cards_frame, height=50, width=50, background=background_color)
vegetable_box.pack(side=LEFT)

vegetable_box_label = tk.Label(vegetable_box, text="Choose your veggies")
vegetable_box_label.pack(pady=10)

vegetable_image = tk.PhotoImage(file="final cards/beef.png")
vegetable_image_label = tk.Label(vegetable_box, image=vegetable_image, background=background_color)
vegetable_image_label.pack()

# Cooking method box
method_box = tk.Frame(scan_cards_frame, height=50, width=50, background=background_color)
method_box.pack(side=LEFT)

method_box_label = tk.Label(vegetable_box, text="Choose your way of cooking", background=background_color)
method_box_label.pack(pady=10)

method_image = tk.PhotoImage(file="final cards/steamed.png")
method_image_label = tk.Label(vegetable_box, image=method_image, background=background_color)
method_image_label.pack()

# Back to home button
back_button = tk.Button(scan_cards_frame, text="Back to Home", command=back_to_home_confirm, image=resized_back_btn).pack(pady=10)

# Continue to results: this will be based on conditional when card is scaneed
continue_button = tk.Button(scan_cards_frame, text="Continue", command=open_results).pack(pady=10)

# Results screen
results_frame = tk.Frame(window, background=background_color)
results_label = tk.Label(results_frame, text="Tadaa!", font=("Roboto", 32))
results_frame.pack(pady=10)

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


open_main()
window.mainloop()