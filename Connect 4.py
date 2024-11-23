import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk



# init players to some token if they do not choose to customize
player1_selection = "Barry"
player2_selection = "Colten"
current_player = 1


def buttonPress(character_name, button):
    global player1_selection, player2_selection, current_player
    
    if current_player == 1:
        if character_name == player2_selection:
            nameLabel.config(text=f"You cannot pick the same character!")
        else:
            player1_selection = character_name
            nameLabel.config(text=f"Player 1 Picked {character_name}")
            button.config(state=tk.DISABLED)
            current_player = 2
    elif current_player == 2:
        if character_name == player1_selection:
            nameLabel.config(text=f"You cannot pick the same character!")
        else:
            player2_selection = character_name
            nameLabel.config(text=f"Player 1 picked {player1_selection}, Player 2 Picked {character_name}")
            button.config(state=tk.DISABLED)
            current_player += 1 # plus 1 to exit loop
            continueButton = tk.Button(root, text="Continue", command=show_main_menu)
            continueButton.grid(row=4, column=0, padx=10, pady=10)

# def game_start_page(): # this page is meant 
#     for widget in root.winfo_children():
#         widget.destroy()
        
#     restart_button = tk.Button(root, text="Restart", command=restart_game)
#     restart_button.pack()

# def restart_game():
#     global player1_selection, player2_selection, current_player
#     player1_selection = None
#     player2_selection = None
#     current_player = 1
#     create_character_selection_window()

# def continueaction(): # continue button, shows after both players have selected a character
#     game_start_page()

def create_button_command(name, button): # code wasn't working but this fixed the error.
    return lambda: buttonPress(name, button)

def create_character_selection_window(): # character selection window 
    global nameLabel,current_player
    print(current_player)
    current_player = 1

    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.grid(row=1, column=0, padx=10, pady=10)

    firstLabel = tk.Label(root, text="Pick a Token!", font=("Arial", 24, "bold"))
    firstLabel.grid(row=0, column=0, columnspan=3, pady=10)

    nameLabel = tk.Label(root)
    nameLabel.grid(row=3, column=0, columnspan=3, pady=15)

    # create buttons and labels for each character
    for i, (image_file, character_name) in enumerate(characters):
        print(f"{image_file}")
        image = Image.open(image_file).convert("RGBA")
        image = image.resize((100, 100))
        tkImage = ImageTk.PhotoImage(image)
        
        button = tk.Button(frame, image=tkImage)
        button.image = tkImage  # avoid garbage collection
        button.grid(row=(i // 3) * 2, column=i % 3, padx=5, pady=5)
        
        # cet the command after the button is created
        button.config(command=create_button_command(character_name, button))
        
        label = tk.Label(frame, text=character_name)
        label.grid(row=(i // 3) * 2 + 1, column=i % 3, padx=5, pady=5)

    exitBtn = tk.Button(root, text="Main Menu", command=show_main_menu)
    exitBtn.grid(row=4, column=1, padx=10, pady=10)

# list of character image filenames and their names
characters = [
    ("Barry.PNG", "Barry"),
    ("Lewis.PNG", "Lewis"),
    ("Noah.PNG", "Noah"),
    ("Colten.PNG", "Colten"),
    ("Twins.PNG", "Twins"),
    ("Zero.PNG", "Zero")
]


def resize_image(filepath, size):
    img = Image.open(filepath).convert("RGBA").resize(size)
    return ImageTk.PhotoImage(img)

def show_main_menu():
    clear_frame()
    tk.Label(root, text="Connect 4", font=("Arial", 24)).pack(pady=20)
    tk.Button(root, text="Play", font=("Arial", 16), command=start_game).pack(pady=10)
    tk.Button(root, text="Token Selection", font=("Arial", 16), command=create_character_selection_window).pack(pady=10)
    tk.Button(root, text="How to Play", font=("Arial", 16), command=show_tutorial).pack(pady=10)
    tk.Button(root, text="Quit", font=("Arial", 16), command=root.quit).pack(pady=10)
game_won = False
def start_game():
    global board, turn, Turn, player_1_image, player_2_image, game_won

    clear_frame()
    Turn = tk.Label(root, text=f"{player1_selection}'s turn!", font=("Arial", 20))
    Turn.pack(pady=20)
    tk.Button(root, text="Main Menu", command=show_main_menu).place(x=10, y=10)
    tk.Button(root, text = "Restart", command=start_game).place(x=550,y=550)
    player_1_image = resize_image(player1_selection + ".PNG", (50, 50))
    player_2_image = resize_image(player2_selection + ".PNG", (50, 50))

    game_won = False
    board = [[0] * 7 for _ in range(6)]
    turn = 1
    create_board()

def create_board():
    global board_frame
    board_frame = tk.Frame(root)
    board_frame.pack()
    
    # transparent placeholder to prevent the button from being resized
    blank_image = Image.new("RGBA", (50, 50), (255, 255, 255, 0))
    blank_photo = ImageTk.PhotoImage(blank_image)
    
    for row in range(6):
        for col in range(7):
            btn = tk.Button(board_frame, image=blank_photo, width=50, height=50, command=lambda r=row, c=col: make_move(r, c),)
            btn.grid(row=row, column=col, padx=2, pady=2)
            btn.image = blank_photo  

def make_move(row, col):
    global turn, game_won
    if game_won: return

    for r in range(5, -1, -1):
        if board[r][col] == 0:
            board[r][col] = turn
            update_button(r, col)
            if check_win():
                # winner = "Player 1" if turn == 1 else "Player 2"
                winner = player1_selection if turn == 1 else player2_selection
                Turn.config(text=f"{winner} won! Congrats!")
                game_won = True
                # Turn.config(text=f"{winner}")
                # messagebox.showinfo("Game Over", f"{winner} wins!") ### REPLACE THIS WITH A LABEL THAT SHOWS SAYING THE WINNER
                # start_game()
            turn = 3 - turn  # fun math trick
            print(turn)
            break

def update_button(row, col):
    print(board)
    players = [player1_selection,player2_selection]
    # tk.Label(root, text = f"{players[turn-1]}'s turn!", font=("Arial", 20)).pack(pady=20)
    Turn.config(text = f"{players[turn-2]}'s turn!")
    image = player_1_image if board[row][col] == 1 else player_2_image
    btn = board_frame.grid_slaves(row=row, column=col)[0]
    btn.configure(image=image, text="", state="disabled", disabledforeground=btn["fg"])
    # btn.image = image



def check_win():
    rows, cols = len(board), len(board[0]) # unpack tuple 

    # defined helper functions inside function for clarity
    def is_within_bounds(x, y): # helper function to check bounds
        return 0 <= x < rows and 0 <= y < cols

    def check_direction(x, y, dx, dy): # helper function
        count = 1
        current = board[x][y]
        nx, ny = x + dx, y + dy
        while is_within_bounds(nx, ny) and board[nx][ny] == current and current != 0:
            count += 1
            if count >= 4:
                return True
            nx += dx
            ny += dy
        return False

    # check thru the board
    for i in range(rows):
        for j in range(cols):
            if board[i][j] in (1, 2): # Ooly check for 1s and 2s since these represent player 1 and 2
                if (check_direction(i, j, 0, 1) or # horizontal
                    check_direction(i, j, 1, 0) or # vertical
                    check_direction(i, j, 1, 1) or # diagonal down-right
                    check_direction(i, j, 1, -1)): # diagonal down-left
                    return True
    return False

def show_tutorial():
    clear_frame()
    tk.Label(root, text="How to Play!", font=("Arial", 20)).pack(pady=20)
    tk.Button(root, text="Main Menu", command=show_main_menu).place(x=10, y=10)
    img_gameplay = resize_image("gameplay.png", (300,250))
    img_label = tk.Label(root,image=img_gameplay)
    img_label.image = img_gameplay
    img_label.place(x=50,y=100)
    txt_box = tk.Label(root, text="The \"Main Menu\" button return you to the main menu.\nThe text at the top of the screen says whose turn it currently is. \nThe name is the same as the token you choose.\nTo restart the game press restart.\nClick on any button that is empty and your token will drop in that column", font=("Arial", 10),justify="left")
    txt_box.place(x=300,y=100)
    img_game = resize_image("board.png",(200,200))
    img_game_label = tk.Label(root,image=img_game)
    img_game_label.place(x=500,y=400)
    img_game_label.image = img_game
    txt_box2 = tk.Label(root,text="Your goal is to get 4 in row whether that is horizontal, vertical, or diagonal!\nA great strategy is to block your opponent like in this picture!",justify="left")
    txt_box2.place(x=100,y=400)

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect 4")
    root.geometry("800x700")
    show_main_menu()
    root.mainloop()
