# In Tkinter, you can use an `if` statement to control when an element pops up on a frame by changing its visibility. Typically, you would use the `pack`, `grid`, or `place` geometry managers to control the placement and visibility of widgets on a frame. Here's a simple example demonstrating how to use an `if` statement to control the visibility of a label on a frame:

import tkinter as tk

def toggle_frame():
    if snd_frame.winfo_ismapped():
        snd_frame.pack_forget()
    else:
        snd_frame.pack() 

# Create the main window
root = tk.Tk()

frame = tk.Frame(root)
frame.pack()
label = tk.Label(frame, text="Hello, world!")
label.pack()

snd_frame = tk.Frame(root)
snd_label = tk.Label(snd_frame, text="kkkk")
snd_frame.pack_forget()

# Create a button to toggle the label's visibility
button = tk.Button(root, text="Open Second frame", command=toggle_frame)
button.pack()

# Run the Tkinter event loop
root.mainloop()