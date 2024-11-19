import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import time

# initial variables for player selection and current player. 
player1_selection = None
player2_selection = None
current_player = 1

def buttonPress(character_name, button):
    global player1_selection, player2_selection, current_player
    
    if current_player == 1:
        player1_selection = character_name
        nameLabel.config(text=f"Player 1 Picked {character_name}")
        button.config(state=DISABLED)  # Disable the button after selection
        current_player = 2
    elif current_player == 2:
        player2_selection = character_name
        nameLabel.config(text=f"Player 1 picked {player1_selection}, Player 2 Picked {character_name}")
        button.config(state=DISABLED)  # Disable the button after selection
        current_player += 1 # plus 1 to exit loop
        continueButton = Button(root, text="Continue", command=continueaction)
        continueButton.grid(row=4, column=0, padx=10, pady=10)

def game_start_page(): # this page is meant 
    for widget in root.winfo_children():
        widget.destroy()
        
    restart_button = Button(root, text="Restart", command=restart_game)
    restart_button.pack()

def restart_game():
    global player1_selection, player2_selection, current_player
    player1_selection = None
    player2_selection = None
    current_player = 1
    create_character_selection_window()

def continueaction(): # continue button, shows after both players have selected a character
    game_start_page()

def create_button_command(name, button): # code wasn't working but this fixed the error.
    return lambda: buttonPress(name, button)

def create_character_selection_window(): # character selection window 
    global nameLabel

    for widget in root.winfo_children():
        widget.destroy()

    frame = Frame(root)
    frame.grid(row=1, column=0, padx=10, pady=10)

    firstLabel = Label(root, text="Pick a Token!", font=("Arial", 24, "bold"))
    firstLabel.grid(row=0, column=0, columnspan=3, pady=10)

    nameLabel = Label(root)
    nameLabel.grid(row=3, column=0, columnspan=3, pady=15)

    # Create buttons and labels for each character
    for i, (image_file, character_name) in enumerate(characters):
        image = Image.open(image_file).convert("RGBA")
        image = image.resize((100, 100))
        tkImage = ImageTk.PhotoImage(image)
        
        button = Button(frame, image=tkImage)
        button.image = tkImage  # Keep a reference to avoid garbage collection
        button.grid(row=(i // 3) * 2, column=i % 3, padx=5, pady=5)
        
        # Set the command after the button is created
        button.config(command=create_button_command(character_name, button))
        
        label = Label(frame, text=character_name)
        label.grid(row=(i // 3) * 2 + 1, column=i % 3, padx=5, pady=5)

    exitBtn = Button(root, text="Exit", command=root.destroy)
    exitBtn.grid(row=4, column=1, padx=10, pady=10)

# List of character image filenames and their names
characters = [
    ("barr.PNG", "Barry"),
    ("lewis.PNG", "Lewis"),
    ("noah.PNG", "Noah"),
    ("colten.PNG", "Colten"),
    ("twins.PNG", "Twins"),
    ("zero.PNG", "Zero")
]

root = Tk()
root.title("Character Selection")

# Start the game by creating the initial character selection window
create_character_selection_window()

root.mainloop()