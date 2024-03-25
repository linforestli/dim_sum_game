import tkinter as tk

def show_instructions():
    main_frame.pack_forget()
    instructions_frame.pack()

def start_game():
    main_frame.pack_forget()
    game_frame.pack()

def back_to_main():
    instructions_frame.pack_forget()
    main_frame.pack()

root = tk.Tk()
root.title("Dim Sum Adventure")

# Main Screen
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

title_label = tk.Label(main_frame, text="Dim Sum Adventure", font=("Helvetica", 24))
title_label.pack(pady=10)

instructions_button = tk.Button(main_frame, text="Instructions", command=show_instructions)
instructions_button.pack(pady=10)

start_game_button = tk.Button(main_frame, text="Start Game", command=start_game)
start_game_button.pack(pady=10)

# Instructions Screen
instructions_frame = tk.Frame(root)

instructions_label = tk.Label(instructions_frame, text="Instructions", font=("Helvetica", 24))
instructions_label.pack(pady=10)

instructions_text = """
Welcome to the Dim Sum Adventure game!

How to play:
- Tap on the ingredient cards to explore different dim sum dishes.
- Learn about the ingredients and history of each dish.
- Enjoy the culinary adventure with your friends!
"""

instructions_text_label = tk.Label(instructions_frame, text=instructions_text)
instructions_text_label.pack(pady=10)

back_button = tk.Button(instructions_frame, text="Back", command=back_to_main)
back_button.pack(pady=10)

# Game Screen (Placeholder)
game_frame = tk.Frame(root)

game_label = tk.Label(game_frame, text="Game Screen", font=("Helvetica", 24))
game_label.pack(pady=10)

back_to_main_button = tk.Button(game_frame, text="Back to Main", command=back_to_main)
back_to_main_button.pack(pady=10)

# Initially show the main frame
show_instructions()
root.mainloop()
